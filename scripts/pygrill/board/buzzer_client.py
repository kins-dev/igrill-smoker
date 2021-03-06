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
import os
# Line to make pylint work
from argparse import ArgumentParser
from Pyro5.api import Proxy
from .buzzer_daemon import Buzzer
from ..common.constant import BUZZ, CONFIG
from . import board
from ..common.local_logging import SetupLog


def main():
    config = configparser.ConfigParser()
    # does not throw an error, just returns the empty set if the file doesn't exist
    config.read(CONFIG.BASEPATH+'/config/iGrill_config.ini')
    loglevel = config.get("Logging", "LogLevel", fallback="Error")
    logfile = config.get("Logging", "LogFile", fallback="")

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
        '--exit',
        dest='shutdown',
        help='Tells the daemon to shutdown',
        action='store_true')

    options = parser.parse_args()

    SetupLog(options.log_level, options.log_destination)

    buzzObj = Proxy(("PYRO:{}@{}:{}").format(
        BUZZ.DAEMON.PYRO_OBJECT_ID,
        BUZZ.DAEMON.PYRO_HOST,
        BUZZ.DAEMON.PYRO_PORT))
    if(options.done):
        buzzObj.Done()
    elif(options.low_battery):
        buzzObj.LowBattery()
    else:
        buzzObj.Stop()
    if(options.shutdown):
        buzzObj.Exit()


if __name__ == '__main__':
    main()
