#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}
source "bt.sh"

echo "Turn on your iGrill now"

BtReset


# stdbuf is needed to prevent buffering of lines
# by hcitool
coproc sudo stdbuf -oL hcitool lescan

while read -r CMD; do

    # when we find the iGrill_V2 setup that information
    if [[ $CMD = *"iGrill"* ]]; then
        MAC=${CMD:0:17}
        echo "$MAC"
        echo -n "ADDRESS='" > mac_config.py
        echo -n "$MAC" >> mac_config.py
        echo "'" >> mac_config.py
        break
    fi
done <&"${COPROC[0]}"

# This will forcably kill the scan
BtReset