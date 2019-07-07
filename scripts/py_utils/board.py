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
from local_logging import SetupLog
import constant

def DetectBoard(board):
    if (constant.SSR_CONTROL_BOARD_DETECT_REV == board):
        pi = pigpio.pi()
        i = 0
        val = 0
        for p in constant.SSR_CONTROL_BOARD_REV_PINS:
            pi.set_mode(p, pigpio.INPUT)

            pi.set_pull_up_down(p, pigpio.PUD_DOWN)
            tmp = pi.read(p)
            logging.debug("Pin \"{}\" : \"{}\"".format(p, tmp))
            val = val + (tmp << i)
            i = i + 1
        logging.debug("Val = \"{}\"".format(val))
    else:
        return board

def main():
    config = configparser.ConfigParser()
    # does not throw an error, just returns the empty set if the file doesn't exist
    config.read(sys.path[0]+'/../../config/iGrill_config.ini')
    loglevel = config.get("Logging", "LogLevel", fallback="Error")
    logfile = config.get("Logging", "LogFile", fallback="")
    board = config.get("SSR", "Board")

    parser = argparse.ArgumentParser(
        description='Sets the leds on the SSR control board')
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

    DetectBoard(board)

if __name__ == '__main__':
    main()