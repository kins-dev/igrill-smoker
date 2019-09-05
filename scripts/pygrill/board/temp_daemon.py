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
import simple_pid
from . import board
from Pyro5.api import expose, behavior, Daemon, Proxy
from ..common.constant import SSRC, TEMP, CONFIG
from ..common.local_logging import SetupLog


@expose
@behavior(instance_mode="single")
class Controller(object):
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
        self.m_pid = simple_pid.PID(
            Kp=TEMP.PID.K_P,
            Ki=TEMP.PID.K_I,
            Kd=TEMP.PID.K_D,
            setpoint=145,
            sample_time=30)
        self.m_pid.output_limits = (TEMP.PID.MIN, TEMP.PID.MAX)

        self.m_active = True
        self.m_threadCondition = threading.Condition()
        self.m_lock = threading.Lock()
        self.m_thread = threading.Thread(target=self.StartThread, args=())
        self.m_thread.start()

    def StartThread(self):
        logging.debug("Starting thread")
        self.m_threadCondition.acquire()
        while(True):
            
            self.m_threadCondition.wait(120.0)
        self.m_threadCondition.release()


    def Adjust(self, temp):
        with(self.m_lock):
            self.m_pid.setpoint = temp

    def FeedBack(self, temp):
        with(self.m_lock):
            self.m_value = self.m_pid(temp)

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
    daemon = Daemon(host=TEMP.DAEMON.PYRO_HOST,
                    port=TEMP.DAEMON.PYRO_PORT)
    tempObj = Controller(daemon)
    uri = daemon.register(
        tempObj, objectId=TEMP.DAEMON.PYRO_OBJECT_ID)
    logging.debug(uri)
    daemon.requestLoop()
    logging.debug('exited requestLoop')
    daemon.shutdown()
    daemon.close()
    logging.debug('daemon closed')
    sys.exit(tempObj.ExitCode())


if __name__ == "__main__":
    main()
