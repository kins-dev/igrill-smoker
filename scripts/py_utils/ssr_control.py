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
from Pyro5.api import Proxy
from local_logging import SetupLog
from kasa_daemon import Kasa
from . import constant
from . import board


config = configparser.ConfigParser()
# does not throw an error, just returns the empty set if the file doesn't exist
config.read(sys.path[0]+'/../../config/iGrill_config.ini')
loglevel = config.get("Logging", "LogLevel", fallback="Error")
logfile = config.get("Logging", "LogFile", fallback="")
board = config.get("SSR", "Board")


parser = argparse.ArgumentParser(
    description='Connects to TP-Link Kasa daemon for power control')
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
    # need target temp, current temp and last temp
    # in band:
        # if need to get warmer and getting warmer - do nothing
        # if need to get colder and getting colder - do nothing
        # if need to stay the same and staying the same - do nothing
        # if need to get warmer and staying the same - up small amount(1%)
        # if need to get warmer and getting colder - up large amount (10%)
        # if need to get colder and getting warmer - down large amount (10%)
        # if need to get colder and staying the same - down small amount (1%)
    # out of band:
        # if need to get warmer - PWM to 100%
        # if need to get colder - PWM to 0%
    # out of band to in band
        # use previous value or pwm is set to 50%
    
    # need to save and restore PWM value for target temp
parser.add_argument(
    '--exit',
    dest='shutdown',
    help='Tells the daemon to shutdown',
    action='store_true')
parser.add_argument(
    '--status',
    dest='status',
    help='Gets the plug state',
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

board = board.DetectBoard(board)

if(0 < len(vars(options))):
    if(options.turn_on and options.turn_off):
        print("Cannot turn on and off at the same time")
        sys.exit(1)

    kasaObj = Proxy(("PYRO:{}@{}:{}").format(
        constant.KASA_DAEMON_PYRO_OBJECT_ID,
        constant.KASA_DAEMON_PYRO_HOST,
        constant.KASA_DAEMON_PYRO_PORT))
    if(options.turn_on):
        kasaObj.TurnPlugOn()
    if(options.turn_off):
        kasaObj.TurnPlugOff()
    if(options.status):
        if(kasaObj.GetActive()):
            print("on")
        else:
            print("off")
    if(options.shutdown):
        kasaObj.Exit()
