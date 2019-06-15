# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file

import sys
import argparse
from Pyro5.api import Proxy
from kasa_daemon import Kasa


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

    # TODO: Move URI parts to ini file
    kasaObj = Proxy("PYRO:Kasa@localhost:9998")
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
