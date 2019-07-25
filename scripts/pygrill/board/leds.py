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

import pigpio
import logging
import argparse
import configparser
import time
import sys
# Line to make pylint work
from argparse import ArgumentParser
from ..common import constant
from . import board
from ..common.local_logging import SetupLog


def SetLED(boardVal, function, desiredValue):
    pi = pigpio.pi()
    item = constant.SSR_CONTROL_BOARD_ITEMS["LED"][function][boardVal]
    value = desiredValue
    if (constant.SSR_CONTROL_BOARD_ITEM_INVALID == item):
        return
    if (constant.SSR_CONTROL_BOARD_VALUES_INVERTED == item[constant.SSR_CONTROL_BOARD_ITEM_VALUE]):
        value = not desiredValue
    writeVal = 0
    if (value):
        writeVal = 1
    pi.set_mode(item[constant.SSR_CONTROL_BOARD_ITEM_IO], pigpio.OUTPUT)
    pi.write(item[constant.SSR_CONTROL_BOARD_ITEM_IO], writeVal)
    return


def main():
    config = configparser.ConfigParser()
    # does not throw an error, just returns the empty set if the file doesn't exist
    config.read(sys.path[0]+'../config/iGrill_config.ini')
    loglevel = config.get("Logging", "LogLevel", fallback="Error")
    logfile = config.get("Logging", "LogFile", fallback="")
    boardVal = config.get("SSR", "Board",  fallback="Auto")

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
        help='Turns on the low battery LED')
    parser.add_argument(
        '--done',
        action='store_true',
        dest='done',
        help='Turns on the smoking complete LED')
    parser.add_argument(
        '--cold',
        action='store_true',
        dest='cold',
        help='Turns on the cold LED')
    parser.add_argument(
        '--cool',
        action='store_true',
        dest='cool',
        help='Turns on the cool LED')
    parser.add_argument(
        '--perfect',
        action='store_true',
        dest='perfect',
        help='Turns on the perfect LED')
    parser.add_argument(
        '--warm',
        action='store_true',
        dest='warm',
        help='Turns on the warm LED')
    parser.add_argument(
        '--hot',
        action='store_true',
        dest='hot',
        help='Turns on the hot LED')
    options = parser.parse_args()

    SetupLog(options.log_level, options.log_destination)

    boardVal = board.DetectBoard(boardVal)
    if (constant.SSR_CONTROL_BOARD_DISABLED == boardVal):
        sys.exit(1)

    SetLED(boardVal, "Smoking complete", options.done)
    SetLED(boardVal, "Low battery", options.low_battery)
    SetLED(boardVal, "Cold", options.cold)
    SetLED(boardVal, "Cool", options.cool)
    SetLED(boardVal, "Perfect", options.perfect)
    SetLED(boardVal, "Warm", options.warm)
    SetLED(boardVal, "Hot", options.hot)


if __name__ == '__main__':
    main()