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
from ..board import leds
from ..common.constant import SSR_CONTROL


class Test_TestLEDs(unittest.TestCase):

    def test_Leds(self):
        with mock.patch('pygrill.board.leds.pigpio.pi') as mockitem:
            mock_pigpio_inst = mockitem.return_value
            for fun in SSR_CONTROL.BOARD_ITEMS["LED"]:
                for board in SSR_CONTROL.BOARD_ITEMS["LED"][fun]:
                    leds.SetLED(board, fun, False)
                    if(SSR_CONTROL.BOARD_VALUES_STANDARD == SSR_CONTROL.BOARD_ITEMS["LED"][fun][board][SSR_CONTROL.BOARD_ITEM_VALUE]):
                        mock_pigpio_inst.write.assert_called_once_with(
                            SSR_CONTROL.BOARD_ITEMS["LED"][fun][board][SSR_CONTROL.BOARD_ITEM_IO], 0)
                    elif(SSR_CONTROL.BOARD_VALUES_INVERTED == SSR_CONTROL.BOARD_ITEMS["LED"][fun][board][SSR_CONTROL.BOARD_ITEM_VALUE]):
                        mock_pigpio_inst.write.assert_called_once_with(
                            SSR_CONTROL.BOARD_ITEMS["LED"][fun][board][SSR_CONTROL.BOARD_ITEM_IO], 1)
                    else:
                        mock_pigpio_inst.write.assert_not_called()
                    mock_pigpio_inst.reset_mock()
                    leds.SetLED(board, fun, True)
                    if(SSR_CONTROL.BOARD_VALUES_STANDARD == SSR_CONTROL.BOARD_ITEMS["LED"][fun][board][SSR_CONTROL.BOARD_ITEM_VALUE]):
                        mock_pigpio_inst.write.assert_called_once_with(
                            SSR_CONTROL.BOARD_ITEMS["LED"][fun][board][SSR_CONTROL.BOARD_ITEM_IO], 1)
                    elif(SSR_CONTROL.BOARD_VALUES_INVERTED == SSR_CONTROL.BOARD_ITEMS["LED"][fun][board][SSR_CONTROL.BOARD_ITEM_VALUE]):
                        mock_pigpio_inst.write.assert_called_once_with(
                            SSR_CONTROL.BOARD_ITEMS["LED"][fun][board][SSR_CONTROL.BOARD_ITEM_IO], 0)
                    else:
                        mock_pigpio_inst.write.assert_not_called()
                    mock_pigpio_inst.reset_mock()


if __name__ == '__main__':
    unittest.main()
