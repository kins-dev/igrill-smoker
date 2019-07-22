from Pyro5.api import expose, behavior, Daemon
import scripts.py_utils
from scripts.py_utils import kasa_daemon
from scripts.py_utils import constant
import unittest

class Test_TestKasaDaemon(unittest.TestCase):

    def test_power(self):
        daemon = Daemon(host=constant.KASA_DAEMON_PYRO_HOST, port=constant.KASA_DAEMON_PYRO_PORT)
        kasaDaemon = kasa_daemon.Kasa(daemon)
        kasaDaemon.TurnPlugOff()
        self.assertEqual(kasaDaemon.GetActive, False)

        kasaDaemon.TurnPlugOn()
        self.assertEqual(kasaDaemon.GetActive, True)
        
        kasaDaemon.TurnPlugOff()
        self.assertEqual(kasaDaemon.GetActive, False)
        daemon.shutdown()
        

    def test_IP(self):
        daemon = Daemon(host=constant.KASA_DAEMON_PYRO_HOST, port=constant.KASA_DAEMON_PYRO_PORT)
        kasaDaemon = kasa_daemon.Kasa(daemon)
        self.assertEqual(kasaDaemon.GetIP(), "192.168.0.23")
        daemon.shutdown()

if __name__ == '__main__':
    unittest.main()