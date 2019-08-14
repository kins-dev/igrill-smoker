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
from ..board import board
from ..common.constant import SSRC


def IoSideEffect_sB(*args, **kwargs):
    io_values = {
        14: 1,
        15: 0,
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


def IoSideEffect_sC(*args, **kwargs):
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


def IoSideEffect_sD(*args, **kwargs):
    io_values = {
        14: 1,
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


def IoSideEffect_sE(*args, **kwargs):
    io_values = {
        14: 0,
        15: 0,
        18: 1,
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

class Test_Board(unittest.TestCase):

    def test_BoardDetect_sB(self):
        #mock_pigpio.read.return_value = 0
        mock_pigpio = mock.Mock()
        mock_pigpio_inst = mock_pigpio.return_value
        mock_pigpio_inst.read.side_effect = IoSideEffect_sB
        with mock.patch('pygrill.board.board.pigpio.pi', mock_pigpio):
            self.assertEqual(board.DetectBoard("Auto"),
                             SSRC.BOARD.REV_sB)
            self.assertEqual(board.DetectBoard("*B"),
                             SSRC.BOARD.REV_sB)

    def test_BoardDetect_sC(self):
        #mock_pigpio.read.return_value = 0
        mock_pigpio = mock.Mock()
        mock_pigpio_inst = mock_pigpio.return_value
        mock_pigpio_inst.read.side_effect = IoSideEffect_sC
        with mock.patch('pygrill.board.board.pigpio.pi', mock_pigpio):
            # print(mock_pigpio.read(15))
            self.assertEqual(board.DetectBoard("Auto"),
                             SSRC.BOARD.REV_sC)
            self.assertEqual(board.DetectBoard("*C"),
                             SSRC.BOARD.REV_sC)

    def test_BoardDetect_sD(self):
        #mock_pigpio.read.return_value = 0
        mock_pigpio = mock.Mock()
        mock_pigpio_inst = mock_pigpio.return_value
        mock_pigpio_inst.read.side_effect = IoSideEffect_sD
        with mock.patch('pygrill.board.board.pigpio.pi', mock_pigpio):
            # print(mock_pigpio.read(15))
            self.assertEqual(board.DetectBoard("Auto"),
                             SSRC.BOARD.REV_sD)
            self.assertEqual(board.DetectBoard("*D"),
                             SSRC.BOARD.REV_sD)

    def test_BoardDetect_sD_patched(self):
        #mock_pigpio.read.return_value = 0
        mock_pigpio = mock.Mock()
        mock_pigpio_inst = mock_pigpio.return_value
        mock_pigpio_inst.read.side_effect = IoSideEffect_sD
        with mock.patch('pygrill.board.board.pigpio.pi', mock_pigpio):
            # print(mock_pigpio.read(15))
            self.assertEqual(board.DetectBoard("Auto"),
                             SSRC.BOARD.REV_sD)
            self.assertEqual(board.DetectBoard("*D.1"),
                             SSRC.BOARD.REV_sD_Patched)

    def test_BoardDetect_sE(self):
        #mock_pigpio.read.return_value = 0
        mock_pigpio = mock.Mock()
        mock_pigpio_inst = mock_pigpio.return_value
        mock_pigpio_inst.read.side_effect = IoSideEffect_sE
        with mock.patch('pygrill.board.board.pigpio.pi', mock_pigpio):
            # print(mock_pigpio.read(15))
            self.assertEqual(board.DetectBoard("Auto"),
                             SSRC.BOARD.REV_sE)
            self.assertEqual(board.DetectBoard("*E"),
                             SSRC.BOARD.REV_sE)

if __name__ == '__main__':
    unittest.main()
