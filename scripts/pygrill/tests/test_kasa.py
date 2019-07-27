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
from Pyro5.api import Daemon
from ..common.local_logging import SetupLog
from ..kasa import kasa_daemon
from ..common import constant


class Test_TestKasaDaemon(unittest.TestCase):

    def test_power(self):
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
            mock_inst.reset_mock()
            mock_inst.recv.return_value = kasa_daemon.EncryptWithHeader(
                b'{"system":{"set_relay_state":{"err_code":0}},"count_down":{"delete_all_rules":{"err_code":0},"add_rule":{"id":"D7F3ED1F8E813522BD9F673AD735E4C3","err_code":0}}}')
            kasaDaemon.TurnPlugOn()
            mock_inst.reset_mock()
            mock_inst.recv.return_value = kasa_daemon.EncryptWithHeader(
                b'{"count_down":{"delete_all_rules":{"err_code":0}},"system":{"set_relay_state":{"err_code":0}}}')
            kasaDaemon.TurnPlugOff()
            mock_inst.reset_mock()
            self.assertEqual(kasaDaemon.GetActive(), False)

            kasaDaemon.Exit()
            daemon.close()
            self.assertEqual(kasaDaemon.ExitCode(), 0)

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


if __name__ == '__main__':
    unittest.main()
