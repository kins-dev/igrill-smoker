# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file

import sys
import Pyro4
from kasa_daemon import Kasa

kasaObj = Pyro4.Proxy("PYRO:Kasa@localhost:9998")

kasaObj.GetIP()
kasaObj.GetActive()