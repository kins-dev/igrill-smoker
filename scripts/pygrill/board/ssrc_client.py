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
import os
import time
import sys
from Pyro5.api import Proxy
from ..common.local_logging import SetupLog
from . import ssrc_daemon
from ..common.constant import SSRC, CONFIG

config = configparser.ConfigParser()
# does not throw an error, just returns the empty set if the file doesn't exist
config.read(CONFIG.BASEPATH+'/config/iGrill_config.ini')
loglevel = config.get("Logging", "LogLevel", fallback="Error")
logfile = config.get("Logging", "LogFile", fallback="")

parser = argparse.ArgumentParser(
    description='Connects to TP-Link Kasa daemon for power control')
parser.add_argument(
    '--cold',
    dest='cold',
    help='The current temp is colder than it should be',
    action='store_true')

parser.add_argument(
    '--hot',
    dest='hot',
    help='The current temp is hotter than it should be',
    action='store_true')

parser.add_argument(
    '--in_band',
    dest='in_band',
    help='The current temp is close to what it should be',
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
    '--status',
    dest='status',
    help='Gets the SSRC status',
    action='store_true')

options = parser.parse_args()

SetupLog(options.log_level, options.log_destination)

if(0 < len(vars(options))):
    if(options.hot and options.cold):
        print("Cannot be too hot and too cold at the same time")
        sys.exit(1)

    ssrcObj = Proxy(("PYRO:{}@{}:{}").format(
        SSRC.DAEMON.PYRO_OBJECT_ID,
        SSRC.DAEMON.PYRO_HOST,
        SSRC.DAEMON.PYRO_PORT))
    # TODO: Put in try except code to handle network errors
    try:
        if(options.shutdown):
            ssrcObj.Exit()
        elif(options.status):
            print("{:.2f}".format(ssrcObj.Status()))
        else:
            if(options.in_band):
                if(options.hot):
                    ssrcObj.Adjust(SSRC.TemperatureState.WARM)
                    logging.debug(
                        "Adjust down 1% to {:.2f}%".format(ssrcObj.Status()))
                elif(options.cold):
                    ssrcObj.Adjust(SSRC.TemperatureState.COOL)
                    logging.debug(
                        "Adjust up 0.25% to {:.2f}%".format(ssrcObj.Status()))
                else:
                    ssrcObj.Adjust(SSRC.TemperatureState.PERFECT)
                    logging.debug(
                        "Stay at {:.2f}%".format(ssrcObj.Status()))
            else:
                if(options.hot):
                    ssrcObj.Adjust(SSRC.TemperatureState.HOT)
                    logging.debug(
                        "Adjust down 20% to {:.2f}%".format(ssrcObj.Status()))
                elif(options.cold):
                    ssrcObj.Adjust(SSRC.TemperatureState.COLD)
                    logging.debug(
                        "Adjust up 5% to {:.2f}%".format(ssrcObj.Status()))
                else:
                    logging.info(
                        "Odd, ssr_client called but not in band, hot or cold, ignoring")
                    # something else like logging
                    pass
    finally:
        # Might get an exception from a communication error (new IP)
        sys.exit(0)