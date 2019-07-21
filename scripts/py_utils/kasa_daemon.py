# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
import socket
import json
import time
import logging
import argparse
import configparser
import sys
from Pyro5.api import expose, behavior, Daemon
from . import constant
from struct import pack
from local_logging import SetupLog

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
    return Decrypt(string[constant.KASA_DAEMON_NET_HEADER_SIZE:])

@expose
@behavior(instance_mode="single")
class Kasa(object):
    def __init__(self, daemon):
        self.m_daemon = daemon
        self.m_tcpSocket = socket.socket()
        self.m_ip = ""
        self.m_active = False
        config = configparser.ConfigParser()
        # does not throw an error, just returns the empty set if the file doesn't exist
        config.read(sys.path[0]+'/../../config/iGrill_config.ini')
        loglevel = config.get("Logging", "LogLevel", fallback="Error")
        logfile = config.get("Logging", "LogFile", fallback="")
        kasa_alias = config.get("Kasa", "Name", fallback="iGrill-smoker")

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
        self.name = kasa_alias
        self.m_findTime = 0
        self.FindDevice()
        self.m_exitCode = 0

    def ExitCode(self):
        return self.m_exitCode

    def FindDevice(self):
        state = -1
        cnt = 0
        # if it has been more than 10 seconds since the last scan, find the device again
        if (10 < (int(time.time()) - self.m_findTime)):
            # Try to discover up to 5 times
            while ((state == -1) and (cnt < 5)):
                self.m_ip, state = self.Discover(self.name)
                cnt += 1
            if (state == -1):
                self.m_exitCode = 1
                self.Exit()
            self.m_active = (state == 1)
            self.m_findTime = int(time.time())
    
    def SendCommand(self, command):
        logging.debug("Setting up socket")
        self.m_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug("Connecting")
        self.m_sock.connect((self.m_ip, constant.KASA_DAEMON_NET_PORT))
        logging.debug("Sending to \"{}\" \"{}\"".format(self.m_ip, command))
        self.m_sock.send(EncryptWithHeader(command))
        logging.debug("Reading result")
        result = DecryptWithHeader(self.m_sock.recv(constant.KASA_DAEMON_NET_BUFFER_SIZE))
        logging.debug("Result: {}".format(result))
        self.m_sock.close()

    def Discover(self, alias):
        logging.debug("Attempting to discover \"{}\"".format(alias))
        logging.debug("Setting up socket")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logging.debug("Allowing broadcast")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        logging.debug("Sending broadcast")
        sock.settimeout(2)
        sock.sendto(Encrypt(constant.KASA_DAEMON_JSON_DISCOVER),(constant.KASA_DAEMON_NET_DISCOVER_IP, constant.KASA_DAEMON_NET_PORT))
        try:
            while (True):
                data, addr = sock.recvfrom(constant.KASA_DAEMON_NET_BUFFER_SIZE)
                json_data = json.loads(Decrypt(data))
                logging.debug("From:     {}".format(addr))
                logging.debug("Received: {}".format(Decrypt(data)))
                if json_data["system"]["get_sysinfo"]["alias"] == alias:
                    logging.debug("Found alias: closing socket")
                    sock.close()
                    return (addr[0], json_data["system"]["get_sysinfo"]["relay_state"])
        except socket.timeout:
            logging.debug("Timeout: closing socket")
            logging.info("\"{}\" was not found, exiting.".format(alias))
            sock.close()
            return ("", -1)

    def GetIP(self):
        self.FindDevice()
        return self.m_ip
    
    def GetActive(self):
        self.FindDevice()
        return self.m_active

    def TurnPlugOn(self):
        self.FindDevice()
        if (self.m_active):
            self.SendCommand(constant.KASA_DAEMON_JSON_COUNTDOWN_DELETE_AND_RUN)
        else:
            self.SendCommand(constant.KASA_DAEMON_JSON_PLUG_ON)
        self.m_active = True        

    def TurnPlugOff(self):
        self.FindDevice()
        if (self.m_active):
            self.SendCommand(constant.KASA_DAEMON_JSON_PLUG_OFF)
        else:
            self.SendCommand(constant.KASA_DAEMON_JSON_COUNTDOWN_DELETE)
        self.m_active = False

    def Exit(self):
        logging.debug("Closing socket")
        self.m_daemon.shutdown()

def main():
    daemon = Daemon(host=constant.KASA_DAEMON_PYRO_HOST, port=constant.KASA_DAEMON_PYRO_PORT)
    kasaObj = Kasa(daemon)
    uri = daemon.register(kasaObj, objectId=constant.KASA_DAEMON_PYRO_OBJECT_ID)
    logging.debug(uri)
    daemon.requestLoop()
    logging.debug('exited requestLoop')
    daemon.close()
    logging.debug('daemon closed')
    sys.exit(kasaObj.ExitCode())

if __name__=="__main__":
    main()