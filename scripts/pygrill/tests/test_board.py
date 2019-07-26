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
from ..board.board import Board
from ..common import constant


def IoSideEffect(*args, **kwargs):
    io_values = {
        14: 0,
        15: 1,
        18: 0,
        23: 0,
        24: 0,
        25: 0,
        8: 0,
        7: 0,
        16: 1,
        20: 1,
        21: 1
    }
    return io_values[args[0]]


class Test_TestBoard(unittest.TestCase):

    @mock.patch("pygrill.board.board.pigpio.pi")
    def test_boardDetect(self, mock_pigpio):
        mock_pigpio.read.return_value = 0
        #mock_pigpio.read.side_effect = IoSideEffect
        print(mock_pigpio.read(15))
        board = Board()
        self.assertEqual(board.DetectBoard("Auto"),
                         constant.SSR_CONTROL_BOARD_REV_sD)
        self.assertEqual(board.DetectBoard("*D"),
                         constant.SSR_CONTROL_BOARD_REV_sD)


if __name__ == '__main__':
    unittest.main()
