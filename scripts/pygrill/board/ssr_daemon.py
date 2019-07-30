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
import sys
from Pyro5.api import expose, behavior, Daemon
from ..common.constant import SSR_CONTROL, SSRC_DAEMON
from . import board
from struct import pack
from ..common.local_logging import SetupLog


@expose
@behavior(instance_mode="single")
class SSR(object):
    def __init__(self, daemon):
        self.m_daemon = daemon
        config = configparser.ConfigParser()
        # does not throw an error, just returns the empty set if the file doesn't exist
        config.read(sys.path[0]+'../config/iGrill_config.ini')
        boardVal = board.DetectBoard(
            config.get("SSR", "Board", fallback="Auto"))
        if (SSR_CONTROL.BOARD_DISABLED == boardVal):
            sys.exit(1)
        self.m_boardVal = boardVal
        self.m_exitCode = 0
        self.m_lowBattery = False
        self.m_done = False
        self.m_active = True
        self.m_lock = threading.Lock()
        self.m_thread = threading.Thread(target=self.StartThread, args=())
        self.m_thread.start()

    def StartThread(self):
        logging.debug("Starting thread")
        pi = pigpio.pi()
        item = SSR_CONTROL.BOARD_ITEMS["SSR"][self.m_boardVal]
        offVal = 1000000
        onVal = offVal // 2
        if item[SSR_CONTROL.BOARD_ITEM_VALUE] == SSR_CONTROL.BOARD_VALUES_STANDARD:
            offVal = 0
        pin = item[SSR_CONTROL.BOARD_ITEM_IO]
        loop_cnt = 0
        loop_val = {
            "low battery": {
                1: {
                    "frequency": 2000,
                    "compare": onVal
                },
                0: {
                    "frequency": 3000,
                    "compare": onVal
                }
            },
            "done": {
                1: {
                    "frequency": 2500,
                    "compare": onVal
                },
                0: {
                    "frequency": 3000,
                    "compare": offVal
                }
            },
            "quiet": {
                1: {
                    "frequency": 2000,
                    "compare": offVal
                },
                0: {
                    "frequency": 3000,
                    "compare": offVal
                }
            }
        }
        while True:
            loop_cnt = loop_cnt + 1
            loop_cnt = loop_cnt % 2
            fun = "quiet"
            with self.m_lock:
                lowBattery = self.m_lowBattery
                done = self.m_done
                active = self.m_active
            if not active:
                pi.hardware_PWM(pin, 2000, offVal)
                break
            if lowBattery:
                logging.debug("Low battery")
                fun = "low battery"
            elif done:
                logging.debug("Done")
                fun = "done"
            else:
                logging.debug("Quiet")
                fun = "quiet"

            pi.hardware_PWM(
                pin, loop_val[fun][loop_cnt]["frequency"], loop_val[fun][loop_cnt]["compare"])
            time.sleep(0.3)

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
        self.m_thread.join()
        logging.debug("Closing socket")
        self.m_daemon.shutdown()


def main():
    config = configparser.ConfigParser()
    # does not throw an error, just returns the empty set if the file doesn't exist
    config.read(sys.path[0]+'/../../config/iGrill_config.ini')
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
    daemon = Daemon(host=SSRC_DAEMON.PYRO_HOST,
                    port=SSRC_DAEMON.PYRO_PORT)
    ssrcObj = SSR(daemon)
    uri = daemon.register(
        ssrcObj, objectId=SSRC_DAEMON.PYRO_OBJECT_ID)
    logging.debug(uri)
    daemon.requestLoop()
    logging.debug('exited requestLoop')
    daemon.close()
    logging.debug('daemon closed')
    sys.exit(ssrcObj.ExitCode())


if __name__ == "__main__":
    main()
