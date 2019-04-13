#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}
echo "Turn on your iGrill2 or iGrill3 now"

function ResetBT()
{
    # Reset BT adapter
    sudo hciconfig hci0 down
    sudo hciconfig hci0 up
}

ResetBT

coproc RunScan (
    # stdbuf is needed to prevent buffering of lines
    # by hcitool
    sudo stdbuf -oL hcitool lescan
)

while read -r CMD; do

    # when we find the iGrill_V2 setup that information
    if [[ $CMD = *"iGrill_"* ]]; then
        MAC=${CMD:0:17}
        echo "$MAC"
        echo -n "ADDRESS='" > mac_config.py
        echo -n "$MAC" >> mac_config.py
        echo "'" >> mac_config.py
        break
    fi
done <&"${RunScan[0]}"

# This will forcably kill the scan
ResetBT