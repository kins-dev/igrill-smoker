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

from Pyro5.api import Daemon
import scripts.py_utils
import kasa_daemon
import constant
import unittest


class Test_TestKasaDaemon(unittest.TestCase):

    def test_power(self):
        daemon = Daemon(host=constant.KASA_DAEMON_PYRO_HOST,
                        port=constant.KASA_DAEMON_PYRO_PORT)
        kasaDaemon = kasa_daemon.Kasa(daemon)
        daemon.register(
            kasaDaemon, objectId=constant.KASA_DAEMON_PYRO_OBJECT_ID)
        kasaDaemon.TurnPlugOff()
        self.assertEqual(kasaDaemon.GetActive(), False)

        kasaDaemon.TurnPlugOn()
        self.assertEqual(kasaDaemon.GetActive(), True)

        kasaDaemon.TurnPlugOff()
        self.assertEqual(kasaDaemon.GetActive(), False)
        kasaDaemon.Exit()
        daemon.close()
        self.assertEqual(kasaDaemon.ExitCode(), 0)

    def test_IP(self):
        daemon = Daemon(host=constant.KASA_DAEMON_PYRO_HOST,
                        port=constant.KASA_DAEMON_PYRO_PORT)
        kasaDaemon = kasa_daemon.Kasa(daemon)
        daemon.register(
            kasaDaemon, objectId=constant.KASA_DAEMON_PYRO_OBJECT_ID)
        self.assertEqual(kasaDaemon.GetIP(), "192.168.0.23")
        kasaDaemon.Exit()
        daemon.close()
        self.assertEqual(kasaDaemon.ExitCode(), 0)

    def test_Exit(self):
        daemon = Daemon(host=constant.KASA_DAEMON_PYRO_HOST,
                        port=constant.KASA_DAEMON_PYRO_PORT)
        kasaDaemon = kasa_daemon.Kasa(daemon)
        daemon.register(
            kasaDaemon, objectId=constant.KASA_DAEMON_PYRO_OBJECT_ID)
        kasaDaemon.Exit()
        daemon.close()
        self.assertEqual(kasaDaemon.ExitCode(), 0)


if __name__ == '__main__':
    unittest.main()
