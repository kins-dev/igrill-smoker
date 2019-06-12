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
import py_utils.constant
from struct import pack
from py_utils.logging import SetupLog
# Encryption and Decryption of TP-Link Kasa Protocol
# XOR Autokey Cipher with starting key = 171
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
	return Decrypt(string[py_utils.constant.KASA_NET_HEADER_SIZE:])

def SendCommand(ip, command):
    logging.debug("Sending to \"{}\" \"{}\"".format(ip, command))
    logging.debug("Setting up socket")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.debug("Connecting")
    sock.connect((ip, py_utils.constant.KASA_NET_PORT))
    logging.debug("Sending JSON data")
    sock.send(EncryptWithHeader(command))
    logging.debug("Reading result")
    result = DecryptWithHeader(sock.recv(py_utils.constant.KASA_NET_BUFFER_SIZE))
    logging.debug("Closing socket")
    sock.close()
    logging.debug("Result: {}".format(result))

def Discover(alias):
    logging.debug("Attempting to discover \"{}\"".format(alias))
    logging.debug("Setting up socket")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logging.debug("Allowing broadcast")
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    logging.debug("Sending broadcast")
    sock.settimeout(2)
    sock.sendto(Encrypt(py_utils.constant.KASA_JSON_DISCOVER),(py_utils.constant.KASA_NET_DISCOVER_IP, py_utils.constant.KASA_NET_PORT))
    try:
        while True:
            data, addr = sock.recvfrom(py_utils.constant.KASA_NET_BUFFER_SIZE)
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
        sys.exit(1)

def TurnOff(alias):
    ip, state = Discover(alias)
    if 0 != state:
        SendCommand(ip, py_utils.constant.KASA_JSON_PLUG_OFF)
    else:
        SendCommand(ip, py_utils.constant.KASA_JSON_COUNTDOWN_DELETE)

def TurnOn(alias):
    ip, state = Discover(alias)
    if 1 != state:
        SendCommand(ip, py_utils.constant.KASA_JSON_PLUG_ON)
    else:
        SendCommand(ip, py_utils.constant.KASA_JSON_COUNTDOWN_DELETE_AND_RUN)

def main():
    print("start")
    config = configparser.ConfigParser()
    # does not throw an error, just returns the empty set if the file doesn't exist
    config.read(sys.path[0]+'/../config/iGrill_config.ini')
    loglevel = config.get("Logging", "LogLevel", fallback="INFO")
    logfile = config.get("Logging", "LogFile", fallback="")
    kasa_alias = config.get("Kasa", "Name", fallback="iGrill-smoker")

    parser = argparse.ArgumentParser(
        description='Connects to iGrill device and calls a script to process results')
    parser.add_argument(
        '--test',
        dest='test_mode',
        help='Test mode, do not run data.sh',
        action='store_true')
    parser.add_argument(
        '--on',
        dest='turn_on',
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
    if (True == options.turn_on):
        logging.info("Turning on plug")
        TurnOn(kasa_alias)
    else:
        logging.info("Turning off plug")
        TurnOff(kasa_alias)
    sys.exit(0)

if __name__ == '__main__':
    main()