#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}
echo "Turn on your iGrill2 or iGrill3 now"
# Reset BT adapter
sudo hciconfig hci0 down
sudo hciconfig hci0 up

coproc RunScan (
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

# Reset BT again
sudo hciconfig hci0 down
sudo hciconfig hci0 up
