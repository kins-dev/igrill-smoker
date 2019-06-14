# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file

import sys
from Pyro5.api import Proxy
from kasa_daemon import Kasa

kasaObj = Proxy("PYRO:Kasa@localhost:9998")

#print(kasaObj.GetIP())
#print(kasaObj.GetActive())
kasaObj.TurnPlugOn()