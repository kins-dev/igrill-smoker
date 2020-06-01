#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# shellcheck source-path=SCRIPTDIR/tests/board
:
# shellcheck disable=2154
set -$-ue${DEBUG+xv}

VALUE=${IGRILL_BAS_DIR:-}
if [ -z "${VALUE}" ]; then
    # https://stackoverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself
    SOURCE="${BASH_SOURCE[0]}"
    while [ -h "${SOURCE}" ]; do # resolve $SOURCE until the file is no longer a symlink
        DIR="$(cd -P "$(dirname "${SOURCE}")" > /dev/null 2>&1 && pwd)"
        SOURCE="$(readlink "${SOURCE}")"
        [[ ${SOURCE} != /* ]] && SOURCE="${DIR}/${SOURCE}" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    done
    DIR="$(cd -P "$(dirname "${SOURCE}")" > /dev/null 2>&1 && pwd)"
    IGRILL_BAS_DIR="$(readlink -f "${DIR}/../..")"
    export IGRILL_BAS_DIR
fi

# shellcheck source=../../scripts/utils/paths.sh
source "${IGRILL_BAS_DIR}/scripts/utils/paths.sh"

echo "Check the smoking complete light is on and hit enter"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --done
read -r
echo "Check the low battery light is on and hit enter"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --low_battery
read -r
echo "Check the cold light is (if supported) on and hit enter"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --cold
read -r
echo "Check the cool light is (if supported) on and hit enter"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --cool
read -r
echo "Check the perfect light (if supported) is on and hit enter"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --perfect
read -r
echo "Check the warm light is (if supported) on and hit enter"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --warm
read -r
echo "Check the hot light is (if supported) on and hit enter"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --hot
read -r
echo "Check the lights are off and hit enter"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds
read -r
echo "Starting buzzer daemon"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.buzzer_daemon --log-level Error &
disown
sleep 1s
echo "Check buzzer turns on and off and hit enter"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.buzzer_client --done
read -r
echo "Check buzzer alternates between two tones and hit enter"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.buzzer_client --low_battery
read -r
echo "Check buzzer is off hit enter"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.buzzer_client
read -r
echo "Shutting down buzzer daemon"
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.buzzer_client --exit
