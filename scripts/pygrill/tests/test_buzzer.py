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

import unittest
import unittest.mock as mock
import time
from Pyro5.api import Daemon
from ..common.local_logging import SetupLog
from ..board import buzzer_daemon
from ..common.constant import SSRC, BUZZ


class Test_BuzzerDaemon(unittest.TestCase):
    def setUp(self):
        self.m_daemon = Daemon(host=BUZZ.DAEMON.PYRO_HOST,
                               port=BUZZ.DAEMON.PYRO_PORT)
        with mock.patch('pygrill.board.buzzer_daemon.pigpio.pi') as mockitem:
            self.m_mock_inst = mockitem.return_value
            self.m_buzzDaemon = buzzer_daemon.Buzzer(
                self.m_daemon, boardIn=SSRC.BOARD.REV_sD)
            self.m_daemon.register(
                self.m_buzzDaemon, objectId=BUZZ.DAEMON.PYRO_OBJECT_ID)

    def tearDown(self):
        self.m_buzzDaemon.Exit()
        self.m_daemon.close()
        self.assertEqual(self.m_buzzDaemon.ExitCode(), 0)

    def test_buzzer(self):
        buzzDaemon = self.m_buzzDaemon
        mock_inst = self.m_mock_inst
        pin = SSRC.BOARD.ITEMS["Buzzer"][SSRC.BOARD.REV_sD][SSRC.BOARD.ITEM_IO]
        mock_inst.hardware_PWM.assert_called_with(pin, 2000, 0)
        buzzDaemon.Done()
        mock_inst.reset_mock()
        time.sleep(0.6)
        mock_inst.hardware_PWM.assert_any_call(pin, 2500, 500000)
        mock_inst.hardware_PWM.assert_any_call(pin, 2500, 0)
        buzzDaemon.LowBattery()
        mock_inst.reset_mock()
        time.sleep(0.6)
        mock_inst.hardware_PWM.assert_any_call(pin, 3000, 500000)
        mock_inst.hardware_PWM.assert_any_call(pin, 2000, 500000)
        buzzDaemon.Stop()
        mock_inst.reset_mock()
        time.sleep(0.1)
        mock_inst.hardware_PWM.assert_called_with(pin, 2000, 0)


if __name__ == '__main__':
    unittest.main()
