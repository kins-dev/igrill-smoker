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
from ..common import constant


class Test_TestLEDs(unittest.TestCase):

    def test_Leds(self):
        with mock.patch('pygrill.board.leds.pigpio.pi') as mockitem:
            mock_pigpio_inst = mockitem.return_value
            for fun in constant.SSR_CONTROL_BOARD_ITEMS["LED"]:
                for board in constant.SSR_CONTROL_BOARD_ITEMS["LED"][fun]:
                    leds.SetLED(board, fun, False)
                    if(constant.SSR_CONTROL_BOARD_VALUES_STANDARD == constant.SSR_CONTROL_BOARD_ITEMS["LED"][fun][board][constant.SSR_CONTROL_BOARD_ITEM_VALUE]):
                        mock_pigpio_inst.write.assert_called_once_with(
                            constant.SSR_CONTROL_BOARD_ITEMS["LED"][fun][board][constant.SSR_CONTROL_BOARD_ITEM_IO], 0)
                    elif(constant.SSR_CONTROL_BOARD_VALUES_INVERTED == constant.SSR_CONTROL_BOARD_ITEMS["LED"][fun][board][constant.SSR_CONTROL_BOARD_ITEM_VALUE]):
                        mock_pigpio_inst.write.assert_called_once_with(
                            constant.SSR_CONTROL_BOARD_ITEMS["LED"][fun][board][constant.SSR_CONTROL_BOARD_ITEM_IO], 1)
                    else:
                        mock_pigpio_inst.write.assert_not_called()
                    mock_pigpio_inst.reset_mock()
                    leds.SetLED(board, fun, True)
                    if(constant.SSR_CONTROL_BOARD_VALUES_STANDARD == constant.SSR_CONTROL_BOARD_ITEMS["LED"][fun][board][constant.SSR_CONTROL_BOARD_ITEM_VALUE]):
                        mock_pigpio_inst.write.assert_called_once_with(
                            constant.SSR_CONTROL_BOARD_ITEMS["LED"][fun][board][constant.SSR_CONTROL_BOARD_ITEM_IO], 1)
                    elif(constant.SSR_CONTROL_BOARD_VALUES_INVERTED == constant.SSR_CONTROL_BOARD_ITEMS["LED"][fun][board][constant.SSR_CONTROL_BOARD_ITEM_VALUE]):
                        mock_pigpio_inst.write.assert_called_once_with(
                            constant.SSR_CONTROL_BOARD_ITEMS["LED"][fun][board][constant.SSR_CONTROL_BOARD_ITEM_IO], 0)
                    else:
                        mock_pigpio_inst.write.assert_not_called()
                    mock_pigpio_inst.reset_mock()


if __name__ == '__main__':
    unittest.main()
