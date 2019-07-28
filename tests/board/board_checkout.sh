#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

pushd ../../scripts
echo "Check the smoking complete light is on and hit enter"
python3 -m pygrill.board.leds --done
read
echo "Check the low battery light is on and hit enter"
python3 -m pygrill.board.leds --low_battery
read
echo "Check the cold light is (if supported) on and hit enter"
python3 -m pygrill.board.leds --cold
read
echo "Check the cool light is (if supported) on and hit enter"
python3 -m pygrill.board.leds --cool
read
echo "Check the perfect light (if supported) is on and hit enter"
python3 -m pygrill.board.leds --perfect
read
echo "Check the warm light is (if supported) on and hit enter"
python3 -m pygrill.board.leds --warm
read
echo "Check the hot light is (if supported) on and hit enter"
python3 -m pygrill.board.leds --hot
read
echo "Check the lights are off and hit enter"
python3 -m pygrill.board.leds
read
popd
