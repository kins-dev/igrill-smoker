#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}
echo "Turn on your iGrill V2 now"
# Reset BT adapter
sudo hciconfig hci0 down
sudo hciconfig hci0 up

# use a FIFO to process each line
mkfifo hci-data
sudo stdbuf -oL hcitool lescan > hci-data &
cat hci-data | \
while read -r CMD; do
    # when we find the iGrill_V2 setup that information
    if [[ $CMD = *"iGrill_V2"* ]]; then
        MAC=${CMD:0:17}
        echo "$MAC"
        echo -n "ADDRESS='" > mac_config.py
        echo -n "$MAC" >> mac_config.py
        echo "'" >> mac_config.py
        break
    fi
done
sudo kill -s int $!
sudo hciconfig hci0 down
rm -f hci-data
sudo hciconfig hci0 up

