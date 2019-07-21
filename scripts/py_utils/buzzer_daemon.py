# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
import pigpio
import time
import logging
import argparse
import configparser
import threading
import sys
from Pyro5.api import expose, behavior, Daemon
import constant
import board
from struct import pack
from local_logging import SetupLog


@expose
@behavior(instance_mode="single")
class Buzzer(object):
    def __init__(self, daemon):
        self.m_daemon = daemon
        config = configparser.ConfigParser()
        # does not throw an error, just returns the empty set if the file doesn't exist
        config.read(sys.path[0]+'/../../config/iGrill_config.ini')
        loglevel = config.get("Logging", "LogLevel", fallback="Error")
        logfile = config.get("Logging", "LogFile", fallback="")
        boardVal = config.get("SSR", "Board")

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
        boardVal = board.DetectBoard(boardVal)
        if (constant.SSR_CONTROL_BOARD_DISABLED == boardVal):
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
        item = constant.SSR_CONTROL_BOARD_ITEMS["Buzzer"][self.m_boardVal]
        offVal = 1000000
        if item[constant.SSR_CONTROL_BOARD_ITEM_VALUE] == constant.SSR_CONTROL_BOARD_VALUES_STANDARD:
            offVal = 0
        pin = item[constant.SSR_CONTROL_BOARD_ITEM_IO]
        while True:
            with self.m_lock:
                lowBattery = self.m_lowBattery
                done = self.m_done
                active = self.m_active
            if not active:
                pi.hardware_PWM(pin,2000,offVal)
                break
            if lowBattery:
                logging.debug("Low battery")
                pi.hardware_PWM(pin,2000,500000)
                time.sleep(0.5)
                pi.hardware_PWM(pin,3000,500000)
                time.sleep(0.5)
            elif done:
                logging.debug("Done")
                pi.hardware_PWM(pin,2500,500000)
                time.sleep(0.5)
                pi.hardware_PWM(pin,2000,offVal)
                time.sleep(0.5)
            else:
                logging.debug("Quiet")
                pi.hardware_PWM(pin,2000,offVal)
                time.sleep(0.5)
                
        # run the thread

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
    daemon = Daemon(host=constant.BUZZ_DAEMON_PYRO_HOST, port=constant.BUZZ_DAEMON_PYRO_PORT)
    buzzObj = Buzzer(daemon)
    uri = daemon.register(buzzObj, objectId=constant.BUZZ_DAEMON_PYRO_OBJECT_ID)
    logging.debug(uri)
    daemon.requestLoop()
    logging.debug('exited requestLoop')
    daemon.close()
    logging.debug('daemon closed')
    sys.exit(buzzObj.ExitCode())

if __name__=="__main__":
    main()