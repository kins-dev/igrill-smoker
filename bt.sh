#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

function BtReset() {
    # turn off the radio and turn it on again
    sudo hciconfig hci0 down
    sudo hciconfig hci0 up
}

true