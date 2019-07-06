# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file

import pigpio
import logging
import argparse
import configparser
import time
import sys
# Line to make pylint work
from argparse import ArgumentParser
import constant
from local_logging import SetupLog

def SetPin(board, color, value):
    pi = pigpio.pi()
    pin = SSR_CONTROL_BOARD_PINS["LED"][color][board]
    pi.write()

def main():
    config = configparser.ConfigParser()
    # does not throw an error, just returns the empty set if the file doesn't exist
    config.read(sys.path[0]+'/../../config/iGrill_config.ini')
    loglevel = config.get("Logging", "LogLevel", fallback="Error")
    logfile = config.get("Logging", "LogFile", fallback="")
    board = config.get("SSR", "Board")

    parser = argparse.ArgumentParser(
        description='Sets the LEDs on the SSR control board')
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
    parser.add_argument(
        '--low_battery',
        action='store_true',
        dest='low_battery',
        help='Turns on the low battery led')
    parser.add_argument(
        '--done',
        action='store_true',
        dest='done',
        help='Turns on the low battery led')
    options = parser.parse_args()

    SetupLog(options.log_level, options.log_destination)


    pi = pigpio.pi()
    pi.set_pad_strength(0,16)
    pi.set_mode(22, pigpio.OUTPUT)
    pi.set_mode(23, pigpio.OUTPUT)

if __name__ == '__main__':
    main()
