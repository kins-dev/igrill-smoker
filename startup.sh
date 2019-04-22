#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

source "bt.sh"
source "leds.sh"

function finish  () {
    # Cleanup on exit
    rm -f /tmp/igrill.json
    rm -f last_temp.sh
    rm -f stage.sh
}

source config.sh
WEBDIR="/var/www/html"
if ! [ -f /tmp/igrill.json ] ; then
    # Setup CSV file
    FILE="$WEBDIR/$(date +"%Y_%m_%d_%I_%M_%p").csv"
    sudo touch "$FILE"
    sudo chmod a+rw "$FILE"
    echo "Time,Battery,Smoke Temp,Food Temp,Internal Target,Smoke Target Low,Smoke Target,Smoke Target High,Plug State" > "$FILE"
    
    # Link CSV file
    sudo rm -f "$CSV_FILE"
    sudo ln -s "$FILE" "$CSV_FILE"
    
    # Setup state file
    sudo touch "$STATE_FILE"
    sudo chmod a+rw "$STATE_FILE"
    sudo bash gen_json.sh
    
    # Cleanup from last run
    rm -f last_temp.sh
    rm -f stage.sh
        
    trap finish INT
    trap finish EXIT
    if [ ! -f "mac_config.py" ]; then
        bash get_mac.sh
    fi
    
    LEDsReset

    # deal with unexpected wireless issues
    while true; do
        # reset the bluetooth connection
        BtReset

        # python may fail if disconnected
        set +e
        python monitor.py
        set -e
    done
    
fi
