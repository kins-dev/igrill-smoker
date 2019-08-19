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
from ..common.constant import SSRC, BUZZ, CONFIG
from . import board
from struct import pack
from ..common.local_logging import SetupLog


@expose
@behavior(instance_mode="single")
class Buzzer(object):
    def __init__(self, daemon, boardIn="Auto"):
        self.m_daemon = daemon
        config = configparser.ConfigParser()
        # does not throw an error, just returns the empty set if the file doesn't exist
        config.read(CONFIG.BASEPATH+'/config/iGrill_config.ini')
        boardVal = board.DetectBoard(
            config.get("SSR", "Board", fallback=boardIn))
        if (SSRC.BOARD.DISABLED == boardVal):
            sys.exit(1)
        self.m_boardVal = boardVal
        self.m_exitCode = 0
        self.m_lowBattery = False
        self.m_done = False
        self.m_active = True
        self.m_threadCondition = threading.Condition()
        self.m_lock = threading.Lock()
        self.m_thread = threading.Thread(target=self.StartThread, args=())
        self.m_thread.start()

    def StartThread(self):
        logging.debug("Starting thread")
        pi = pigpio.pi()
        item = SSRC.BOARD.ITEMS["Buzzer"][self.m_boardVal]
        onVal = BUZZ.PWM.MAX // 2  # integer division
        if item[SSRC.BOARD.ITEM_VALUE] == SSRC.BOARD.VALUES_STANDARD:
            offVal = BUZZ.PWM.MIN
        else:
            offVal = BUZZ.PWM.MAX
        pin = item[SSRC.BOARD.ITEM_IO]
        loop_cnt = 0
        loop_val = {
            "low battery": {
                1: {
                    "frequency": BUZZ.PWM.FREQ1,
                    "compare": onVal
                },
                0: {
                    "frequency": BUZZ.PWM.FREQ3,
                    "compare": onVal
                }
            },
            "done": {
                1: {
                    "frequency": BUZZ.PWM.FREQ2,
                    "compare": onVal
                },
                0: {
                    "frequency": BUZZ.PWM.FREQ2,
                    "compare": offVal
                }
            },
            "quiet": {
                1: {
                    "frequency": BUZZ.PWM.FREQ1,
                    "compare": offVal
                },
                0: {
                    "frequency": BUZZ.PWM.FREQ1,
                    "compare": offVal
                }
            }
        }
        self.m_threadCondition.acquire()
        while True:
            loop_cnt = loop_cnt + 1
            loop_cnt = loop_cnt % 2
            fun = "quiet"
            with self.m_lock:
                lowBattery = self.m_lowBattery
                done = self.m_done
                active = self.m_active
            if not active:
                pi.hardware_PWM(pin, BUZZ.PWM.FREQ1, offVal)
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
            self.m_threadCondition.wait(0.5)
        self.m_threadCondition.release()

    def Done(self):
        logging.debug("Starting done buzzer")
        with self.m_lock:
            self.m_done = True
            self.m_lowBattery = False
        self.m_threadCondition.acquire()
        self.m_threadCondition.notify()
        self.m_threadCondition.release()

    def LowBattery(self):
        logging.debug("Starting low battery buzzer")
        with self.m_lock:
            self.m_done = False
            self.m_lowBattery = True
        self.m_threadCondition.acquire()
        self.m_threadCondition.notify()
        self.m_threadCondition.release()

    def Stop(self):
        logging.debug("Stopping buzzer")
        with self.m_lock:
            self.m_done = False
            self.m_lowBattery = False
        self.m_threadCondition.acquire()
        self.m_threadCondition.notify()
        self.m_threadCondition.release()

    def ExitCode(self):
        return self.m_exitCode

    def Exit(self):
        with self.m_lock:
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
    config.read(CONFIG.BASEPATH+'/config/iGrill_config.ini')
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
    daemon = Daemon(host=BUZZ.DAEMON.PYRO_HOST,
                    port=BUZZ.DAEMON.PYRO_PORT)
    buzzObj = Buzzer(daemon)
    uri = daemon.register(
        buzzObj, objectId=BUZZ.DAEMON.PYRO_OBJECT_ID)
    logging.debug(uri)
    daemon.requestLoop()
    logging.debug('exited requestLoop')
    daemon.close()
    logging.debug('daemon closed')
    sys.exit(buzzObj.ExitCode())


if __name__ == "__main__":
    main()
