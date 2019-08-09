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

import sys
import argparse
from Pyro5.api import Proxy
from .kasa_daemon import Kasa
from ..common.constant import KASA


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
options = parser.parse_args()

if(0 < len(vars(options))):
    if(options.turn_on and options.turn_off):
        print("Cannot turn on and off at the same time")
        sys.exit(1)

    kasaObj = Proxy(("PYRO:{}@{}:{}").format(
        KASA.DAEMON.PYRO_OBJECT_ID,
        KASA.DAEMON.PYRO_HOST,
        KASA.DAEMON.PYRO_PORT))
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
