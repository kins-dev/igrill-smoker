#!/usr/bin/env python3
"""
  Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
                        (https://git.kins.dev/igrill-smoker)
  License:              MIT License
                        See the LICENSE file
"""

__author__ = "Scott Atkins"
__version__ = "1.4.0"
__license__ = "MIT"

import socket
import json
import time
import logging
import argparse
import os
import configparser
import sys
from Pyro5.api import expose, behavior, Daemon
from struct import pack
from ..common.constant import KASA, CONFIG
from ..common.local_logging import SetupLog


def Encrypt(string):
    key = 171
    result = bytearray()
    for i in string:
        a = key ^ i
        key = a
        result.append(a)
    return result


def EncryptWithHeader(string):
    result = bytearray(pack('>I', len(string)))
    result += Encrypt(string)
    return result


def Decrypt(string):
    key = 171
    result = ""
    for i in string:
        a = key ^ i
        key = i
        result += chr(a)
    return result


def DecryptWithHeader(string):
    return Decrypt(string[KASA.DAEMON.NET_HEADER_SIZE:])


@expose
@behavior(instance_mode="single")
class Kasa(object):
    def __init__(self, daemon):
        #SetupLog("Debug", "")
        self.m_daemon = daemon
        self.m_tcpSocket = socket.socket()
        self.m_ip = ""
        self.m_active = False
        config = configparser.ConfigParser()
        # does not throw an error, just returns the empty set if the file doesn't exist
        config.read(CONFIG.BASEPATH+'/config/iGrill_config.ini')
        kasa_alias = config.get("Kasa", "Name", fallback="iGrill-smoker")

        self.m_name = kasa_alias
        self.m_findTime = 0
        self.m_exitCode = 0
        self.m_errors = list()
        self.m_fail_cnt = 0
        self.m_discovery_fail_cnt = 0
        self.m_ip = ""
        self.m_ipValid = False
        self.GetSystemInfo()

    def ExitCode(self):
        return self.m_exitCode

    def CheckForErrors(self, result):
        data = json.loads(result)
        if(len(data) > 0):
            for system in data:
                if(len(data[system]) > 0):
                    for command in data[system]:
                        val = data[system][command].get('err_code', -1)
                        if(0 != val):
                            self.m_errors.append(result)
                else:
                    self.m_errors.append(result)
        else:
            self.m_errors.append(result)

    def SendCommand(self, command):
        result = ""
        if (3 < self.m_fail_cnt or False == self.m_ipValid):
            self.m_ipValid = False
            self.m_ip = ""
            self.Discover()
        if (self.m_ipValid):
            logging.debug("Setting up socket")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.debug("Connecting")
            try:
                sock.connect((self.m_ip, KASA.DAEMON.NET_PORT))
                logging.debug("Sending to \"{}:{}\" \"{}\"".format(
                    self.m_ip, KASA.DAEMON.NET_PORT, command))
                sock.send(EncryptWithHeader(command))
                logging.debug("Reading result")
                result = DecryptWithHeader(
                    sock.recv(KASA.DAEMON.NET_BUFFER_SIZE))
                logging.debug("Result: {}".format(result))
                self.CheckForErrors(result)
            except socket.error as e:
                logging.error("Socket error {} while trying to communicate".format(e))
                self.m_fail_cnt = self.m_fail_cnt + 1
            finally:
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
        return result

    def GetSystemInfo(self):
        result = self.SendCommand(KASA.DAEMON.JSON_DISCOVER)
        if("" != result):
            data = json.loads(result)
            self.m_active = (1 == data["system"]["get_sysinfo"]["relay_state"])


    def Discover(self):
        logging.debug("Attempting to discover \"{}\"".format(self.m_name))
        logging.debug("Setting up socket")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logging.debug("Allowing broadcast")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        logging.debug("Sending broadcast")
        sock.settimeout(2 + self.m_fail_cnt)
        logging.debug("Msg: {}".format(KASA.DAEMON.JSON_DISCOVER))
        logging.debug("To:  {}:{}".format(
            KASA.DAEMON.NET_DISCOVER_IP, KASA.DAEMON.NET_PORT))
        sock.sendto(Encrypt(KASA.DAEMON.JSON_DISCOVER),
                    (KASA.DAEMON.NET_DISCOVER_IP, KASA.DAEMON.NET_PORT))
        try:
            while (True):
                data, addr = sock.recvfrom(
                    KASA.DAEMON.NET_BUFFER_SIZE)
                json_data = json.loads(Decrypt(data))
                logging.debug("From:     {}".format(addr))
                logging.debug("Received: {}".format(Decrypt(data)))
                if (json_data["system"]["get_sysinfo"]["alias"] == self.m_name):
                    logging.debug("Found alias: closing socket")
                    self.m_ip = addr[0]
                    self.m_ipValid = True
                    self.m_discovery_fail_cnt = 0
                    self.m_fail_cnt = 0
                    break
        except socket.timeout:
            self.m_discovery_fail_cnt = self.m_discovery_fail_cnt + 1
            logging.info("Timed out while looking for \"{}\"".format(self.m_name))
            if(10 <= self.m_discovery_fail_cnt):
                logging.error("Failed to discover {} times".format(self.m_discovery_fail_cnt))
        finally:
            sock.close()

    def GetIP(self):
        if(False == self.m_ipValid):
            self.GetSystemInfo()
        return self.m_ip

    def GetActive(self):
        self.GetSystemInfo()
        return self.m_active

    def GetErrors(self):
        return self.m_errors

    def ClearErrors(self):
        self.m_errors = list()

    def TurnPlugOn(self):
        self.GetSystemInfo()
        if (self.m_active):
            self.SendCommand(KASA.DAEMON.JSON_COUNTDOWN_DELETE_AND_RUN)
        else:
            self.SendCommand(KASA.DAEMON.JSON_PLUG_ON)
        self.m_active = True

    def TurnPlugOff(self):
        self.GetSystemInfo()
        if (self.m_active):
            self.SendCommand(KASA.DAEMON.JSON_PLUG_OFF)
        else:
            self.SendCommand(KASA.DAEMON.JSON_COUNTDOWN_DELETE)
        self.m_active = False

    def Exit(self):
        logging.debug("Closing socket")
        self.m_daemon.shutdown(socket.SHUT_RDWR)


def main():
    config = configparser.ConfigParser()
    # does not throw an error, just returns the empty set if the file doesn't exist
    config.read(CONFIG.BASEPATH+'/config/iGrill_config.ini')
    loglevel = config.get("Logging", "LogLevel", fallback="Error")
    logfile = config.get("Logging", "LogFile", fallback="")

    parser = argparse.ArgumentParser(
        description='Connects to TP-Link Kasa hardware for power control')
    parser.add_argument(
        '-l',
        '--log-level',
        action='store',
        dest='log_level',
        default=loglevel,
        help='Set log level, default: \'' + loglevel + '\'')
    parser.add_argument(
        '-d',
        '--log-destination',
        action='store',
        dest='log_destination',
        default=logfile,
        help='Set log destination (file), default: \'' + logfile + '\'')
    options = parser.parse_args()

    SetupLog(options.log_level, options.log_destination)
    daemon = Daemon(host=KASA.DAEMON.PYRO_HOST,
                    port=KASA.DAEMON.PYRO_PORT)
    kasaObj = Kasa(daemon)
    uri = daemon.register(
        kasaObj, objectId=KASA.DAEMON.PYRO_OBJECT_ID)
    logging.debug(uri)
    daemon.requestLoop()
    logging.debug('exited requestLoop')
    daemon.shutdown()
    daemon.close()
    logging.debug('daemon closed')
    sys.exit(kasaObj.ExitCode())


if __name__ == "__main__":
    main()
