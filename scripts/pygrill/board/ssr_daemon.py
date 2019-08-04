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
import time
import logging
import argparse
import configparser
import threading
import os
import sys
from Pyro5.api import expose, behavior, Daemon
from ..common.constant import SSRC
from . import board
from struct import pack
from ..common.local_logging import SetupLog


@expose
@behavior(instance_mode="single")
class Relay(object):
    def __init__(self, daemon, boardIn="Auto"):
        self.m_daemon = daemon
        config = configparser.ConfigParser()
        # does not throw an error, just returns the empty set if the file doesn't exist
        config.read(sys.path[0]+'../config/iGrill_config.ini')
        boardVal = board.DetectBoard(
            config.get("SSR", "Board", fallback=boardIn))
        if (SSRC.BOARD.DISABLED == boardVal):
            sys.exit(1)
        self.m_boardVal = boardVal
        self.m_exitCode = 0
        self.m_currentCompare = SSRC.TemperatureLimits.MIN
        self.m_active = True
        self.m_threadCondition = threading.Condition()
        self.m_lock = threading.Lock()
        self.m_thread = threading.Thread(target=self.StartThread, args=())
        self.m_thread.start()

    def StartThread(self):
        logging.debug("Starting thread")
        pi = pigpio.pi()
        item = SSRC.BOARD.ITEMS["Relay"][self.m_boardVal]
        offVal = 1000000
        if item[SSRC.BOARD.ITEM_VALUE] == SSRC.BOARD.VALUES_STANDARD:
            offVal = 0
        pin = item[SSRC.BOARD.ITEM_IO]
        self.m_threadCondition.acquire()
        while True:
            with self.m_lock:
                active = self.m_active
                currentCompare = self.m_currentCompare
            if not active:
                pi.hardware_PWM(pin, 2000, offVal)
                break

            pi.hardware_PWM(pin, 101, currentCompare)
            self.m_threadCondition.wait(120.0)
        self.m_threadCondition.release()

    def Done(self):
        logging.debug("Starting done buzzer")
        self.m_done = True
        self.m_lowBattery = False

    def LowBattery(self):
        logging.debug("Starting low battery buzzer")
        self.m_done = False
        self.m_lowBattery = True

    def Stop(self):
        logging.debug("Stopping buzzer")
        self.m_done = False
        self.m_lowBattery = False

    def ExitCode(self):
        return self.m_exitCode

    def Exit(self):
        self.m_active = False
        self.m_threadCondition.acquire()
        self.m_threadCondition.notify()
        self.m_threadCondition.release()
        self.m_thread.join()
        logging.debug("Closing socket")
        self.m_daemon.shutdown()


def main():
    config = configparser.ConfigParser()
    # does not throw an error, just returns the empty set if the file doesn't exist
    if not 'IGRILL_CFG_DIR' in os.environ:
        config.read(sys.path[0]+'/../../config/iGrill_config.ini')
    else:
        config.read(os.environ['IGRILL_CFG_DIR']+'/iGrill_config.ini')
    loglevel = config.get("Logging", "LogLevel", fallback="Error")
    logfile = config.get("Logging", "LogFile", fallback="")

    parser = argparse.ArgumentParser(
        description='Runs a thread to control the buzzer')
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
    daemon = Daemon(host=SSRC.DAEMON.PYRO_HOST,
                    port=SSRC.DAEMON.PYRO_PORT)
    ssrcObj = Relay(daemon)
    uri = daemon.register(
        ssrcObj, objectId=SSRC.DAEMON.PYRO_OBJECT_ID)
    logging.debug(uri)
    daemon.requestLoop()
    logging.debug('exited requestLoop')
    daemon.close()
    logging.debug('daemon closed')
    sys.exit(ssrcObj.ExitCode())


if __name__ == "__main__":
    main()
