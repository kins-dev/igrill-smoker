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
import Pyro4
import constant
from struct import pack
from locallogging import SetupLog

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
    return Decrypt(string[constant.KASA_NET_HEADER_SIZE:])

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Kasa(object):
    def __init__(self, daemon):
        self.m_daemon = daemon
        self.m_tcpSocket = socket.socket()
        self.m_ip = ""
        self.m_active = False
        config = configparser.ConfigParser()
        # does not throw an error, just returns the empty set if the file doesn't exist
        config.read(sys.path[0]+'/../../config/iGrill_config.ini')
        loglevel = config.get("Logging", "LogLevel", fallback="INFO")
        logfile = config.get("Logging", "LogFile", fallback="")
        kasa_alias = config.get("Kasa", "Name", fallback="iGrill-smoker")

        parser = argparse.ArgumentParser(
            description='Connects to iGrill device and calls a script to process results')
        parser.add_argument(
            '--on',
            dest='turn_on',
            help='Turns the plug on, with a 5 minute countdown to turn off if no other command comes in',
            action='store_true')
        parser.add_argument(
            '--off',
            dest='turn_off',
            help='Turns the plug on, with a 5 minute countdown to turn off if no other command comes in',
            action='store_true')
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
        self.m_ip, state = self.Discover(kasa_alias)
        self.m_active = (state == 1)
        logging.debug("Setting up socket")
        self.m_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug("Connecting")
        self.m_sock.connect((self.m_ip, constant.KASA_NET_PORT))
    
    def SendCommand(self, ip, command):
        logging.debug("Sending to \"{}\" \"{}\"".format(ip, command))
        self.m_sock.send(EncryptWithHeader(command))
        logging.debug("Reading result")
        result = DecryptWithHeader(self.m_sock.recv(constant.KASA_NET_BUFFER_SIZE))
        logging.debug("Result: {}".format(result))

    def Discover(self, alias):
        logging.debug("Attempting to discover \"{}\"".format(alias))
        logging.debug("Setting up socket")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logging.debug("Allowing broadcast")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        logging.debug("Sending broadcast")
        sock.settimeout(2)
        sock.sendto(Encrypt(constant.KASA_JSON_DISCOVER),(constant.KASA_NET_DISCOVER_IP, constant.KASA_NET_PORT))
        try:
            while True:
                data, addr = sock.recvfrom(constant.KASA_NET_BUFFER_SIZE)
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

    def GetIP(self):
        return self.m_ip
    
    def GetActive(self):
        return self.m_active

    def TurnPlugOn(self):
        pass

    def Exit(self):
        logging.debug("Closing socket")
        self.m_sock.close()
        self.m_daemon.shutdown()

def main():
    daemon = Pyro4.Daemon(port=9998, host="localhost")
    kasaObj = Kasa(daemon)
    uri = daemon.register(kasaObj, objectId='Kasa')
    print(uri)
    daemon.requestLoop()
    print('exited requestLoop')
    daemon.close()
    print('daemon closed')

if __name__=="__main__":
    main()