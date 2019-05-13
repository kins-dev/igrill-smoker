#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}
function LEDsReset() {
    # Turn off LEDs
    gpio mode 15 out
    gpio write 15 1
    gpio mode 4 out
    gpio write 4 0

}

function LEDsSetState () {
    if [ "$#" -ne "2" ]; then
        echo "Wrong number of arguments to SetLEDState"
        echo "Expected 2, got $#"
        exit 1
    fi
    local COLOR="$1"
    local VALUE="$2"
    local ON_VAL="1"
    local OFF_VAL="0"
    local GPIO
    # TODO: Document pin hookups
    case "$COLOR" in
        "red")
            GPIO="4"
        ;;
        "green")
            GPIO="15"
            OFF_VAL="1"
            ON_VAL="0"
        ;;
        *)
            echo "bad value for led sent to SetLEDState"
            echo "expected \"red\" or \"green\", got \"$COLOR\""
            exit 1
        ;;
    esac
    case "$VALUE" in
        "on")
            gpio write "$GPIO" "$ON_VAL" &
        ;;
        "off")
            gpio write "$GPIO" "$OFF_VAL" &
        ;;
        *)
            echo "bad value for LED state sent to SetLEDState"
            echo "expected \"on\" or \"off\", got \"$VALUE\""
            exit 1
        ;;
    esac
    echo "Turning LED $COLOR $VALUE"
}