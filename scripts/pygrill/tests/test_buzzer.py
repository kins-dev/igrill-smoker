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
        time.sleep(0.7)
        mock_inst.hardware_PWM.assert_any_call(pin, 2500, 500000)
        mock_inst.hardware_PWM.assert_any_call(pin, 2500, 0)
        buzzDaemon.LowBattery()
        mock_inst.reset_mock()
        time.sleep(0.7)
        mock_inst.hardware_PWM.assert_any_call(pin, 3000, 500000)
        mock_inst.hardware_PWM.assert_any_call(pin, 2000, 500000)
        buzzDaemon.Stop()
        mock_inst.reset_mock()
        time.sleep(0.4)
        mock_inst.hardware_PWM.assert_called_with(pin, 2000, 0)

    """
    def test_IP(self):
        daemon = Daemon(host=constant.KASA_DAEMON_PYRO_HOST,
                        port=constant.KASA_DAEMON_PYRO_PORT)
        with mock.patch('pygrill.kasa.kasa_daemon.socket.socket') as mockitem:
            mock_inst = mockitem.return_value
            mock_inst.recvfrom.return_value = [kasa_daemon.Encrypt(
                b'{"system":{"get_sysinfo":{"sw_ver":"0 Build 0 Rel.0","hw_ver":"0.0","type":"IOT.SMARTPLUGSWITCH","model":"00000(XX)","mac":"00:00:00:00:00:00","dev_name":"Wi-Fi Plug","alias":"iGrill-smoker","relay_state":0,"on_time":0,"active_mode":"none","feature":"TIM","updating":0,"icon_hash":"","rssi":-55,"led_off":0,"longitude_i":0,"latitude_i":0,"hwId":"0","fwId":"00000000000000000000000000000000","deviceId":"0","oemId":"0","err_code":0}}}'),
                ['192.168.0.0', 9999]]
            kasaDaemon = kasa_daemon.Kasa(daemon)
            daemon.register(
                kasaDaemon, objectId=constant.KASA_DAEMON_PYRO_OBJECT_ID)
            self.assertEqual(kasaDaemon.GetIP(), "192.168.0.0")
            kasaDaemon.Exit()
            daemon.close()
            self.assertEqual(kasaDaemon.ExitCode(), 0)

    def test_Exit(self):
        daemon = Daemon(host=constant.KASA_DAEMON_PYRO_HOST,
                        port=constant.KASA_DAEMON_PYRO_PORT)
        with mock.patch('pygrill.kasa.kasa_daemon.socket.socket') as mockitem:
            mock_inst = mockitem.return_value
            mock_inst.recvfrom.return_value = [kasa_daemon.Encrypt(
                b'{"system":{"get_sysinfo":{"sw_ver":"0 Build 0 Rel.0","hw_ver":"0.0","type":"IOT.SMARTPLUGSWITCH","model":"00000(XX)","mac":"00:00:00:00:00:00","dev_name":"Wi-Fi Plug","alias":"iGrill-smoker","relay_state":0,"on_time":0,"active_mode":"none","feature":"TIM","updating":0,"icon_hash":"","rssi":-55,"led_off":0,"longitude_i":0,"latitude_i":0,"hwId":"0","fwId":"00000000000000000000000000000000","deviceId":"0","oemId":"0","err_code":0}}}'),
                ['192.168.0.0', 9999]]
            kasaDaemon = kasa_daemon.Kasa(daemon)
            daemon.register(
                kasaDaemon, objectId=constant.KASA_DAEMON_PYRO_OBJECT_ID)
            kasaDaemon.Exit()
            daemon.close()
            self.assertEqual(kasaDaemon.ExitCode(), 0)
    """


if __name__ == '__main__':
    unittest.main()
