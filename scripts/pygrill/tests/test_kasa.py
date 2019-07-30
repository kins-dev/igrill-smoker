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

import time
import unittest
import unittest.mock as mock
from Pyro5.api import Daemon
from ..common.local_logging import SetupLog
from ..kasa import kasa_daemon
from ..common.constant import KASA, TEST


class Test_KasaDaemon(unittest.TestCase):

    def setUp(self):
        self.m_daemon = Daemon(host=KASA.DAEMON.PYRO_HOST,
                               port=KASA.DAEMON.PYRO_PORT)
        # This must be scoped oddly.  Daemon uses sockets so we don't want to mock the socket
        # object untill the daemon is setup.
        with mock.patch('pygrill.kasa.kasa_daemon.socket.socket') as mockitem:
            self.m_mock_inst = mockitem.return_value
            self.m_mock_inst.recvfrom.return_value = [kasa_daemon.Encrypt(
                TEST.KASA.DAEMON.DISCOVER_RSP), ['192.168.0.0', 9999]]
            self.m_kasaDaemon = kasa_daemon.Kasa(self.m_daemon)
            self.m_daemon.register(
                self.m_kasaDaemon, objectId=KASA.DAEMON.PYRO_OBJECT_ID)

    def tearDown(self):
        self.m_kasaDaemon.Exit()
        self.m_daemon.close()
        self.assertEqual(self.m_kasaDaemon.ExitCode(), 0)

    def test_Power(self):
        # Since the above mock is out of scope, we must create a new mock here
        with mock.patch('pygrill.kasa.kasa_daemon.socket.socket') as mockitem:
            mock_inst = mockitem.return_value
            mock_inst.recv.return_value = kasa_daemon.EncryptWithHeader(
                TEST.KASA.DAEMON.ON_NO_ERROR_RSP)
            self.m_kasaDaemon.TurnPlugOn()
            self.assertListEqual(self.m_kasaDaemon.GetErrors(), list())
            mock_inst.send.assert_called_with(
                kasa_daemon.EncryptWithHeader(KASA.DAEMON.JSON_PLUG_ON))
            mock_inst.reset_mock()
            mock_inst.recv.return_value = kasa_daemon.EncryptWithHeader(
                TEST.KASA.DAEMON.ON_NO_ERROR_RSP)
            self.m_kasaDaemon.TurnPlugOn()
            self.assertListEqual(self.m_kasaDaemon.GetErrors(), list())
            mock_inst.send.assert_called_with(
                kasa_daemon.EncryptWithHeader(KASA.DAEMON.JSON_COUNTDOWN_DELETE_AND_RUN))
            mock_inst.reset_mock()
            mock_inst.recv.return_value = kasa_daemon.EncryptWithHeader(
                TEST.KASA.DAEMON.OFF_NO_ERROR_RSP)
            self.m_kasaDaemon.TurnPlugOff()
            self.assertListEqual(self.m_kasaDaemon.GetErrors(), list())
            mock_inst.send.assert_called_with(
                kasa_daemon.EncryptWithHeader(KASA.DAEMON.JSON_PLUG_OFF))
            mock_inst.reset_mock()
            mock_inst.recv.return_value = kasa_daemon.EncryptWithHeader(
                TEST.KASA.DAEMON.OFF_NO_ERROR_RSP)
            self.m_kasaDaemon.TurnPlugOff()
            self.assertListEqual(self.m_kasaDaemon.GetErrors(), list())
            mock_inst.send.assert_called_with(
                kasa_daemon.EncryptWithHeader(KASA.DAEMON.JSON_COUNTDOWN_DELETE))
            mock_inst.reset_mock()
            mock_inst.recv.return_value = kasa_daemon.EncryptWithHeader(
                TEST.KASA.DAEMON.OFF_NO_ERROR_RSP)
            self.m_kasaDaemon.TurnPlugOff()
            self.assertListEqual(self.m_kasaDaemon.GetErrors(), list())
            mock_inst.send.assert_called_with(
                kasa_daemon.EncryptWithHeader(KASA.DAEMON.JSON_PLUG_ON))
            mock_inst.reset_mock()
            mock_inst.recv.return_value = kasa_daemon.EncryptWithHeader(
                TEST.KASA.DAEMON.OFF_ERROR_RSP)
            self.m_kasaDaemon.TurnPlugOff()
            resp = list()
            resp.append(kasa_daemon.Decrypt(
                kasa_daemon.Encrypt(TEST.KASA.DAEMON.OFF_ERROR_RSP)))
            self.assertListEqual(self.m_kasaDaemon.GetErrors(), resp)
            mock_inst.send.assert_called()
            mock_inst.reset_mock()

            self.assertEqual(self.m_kasaDaemon.GetActive(), False)

    def test_IP(self):
        self.assertEqual(self.m_kasaDaemon.GetIP(), "192.168.0.0")


if __name__ == '__main__':
    unittest.main()
