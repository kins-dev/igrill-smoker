#!/bin/bash
set -ue
source config.sh
WEBDIR="/var/www/html"
if ! [ -f /tmp/igrill.json ] ; then
    FILE="$WEBDIR/$(date +"%Y_%m_%d_%I_%M_%p").csv"
    sudo touch $FILE
    sudo touch $STATE_FILE
    sudo chmod a+rw $STATE_FILE
    sudo chmod a+rw $FILE
    echo "Time,Battery,Smoke Temp,Food Temp,Internal Target,Smoke Target Low,Smoke Target,Smoke Target High,Plug State" > $FILE
    sudo rm -f $CSV_FILE
    sudo ln -s $FILE $CSV_FILE
    sudo bash gen_json.sh
    rm -f last_temp.sh
    rm -f stage.sh
    gpio mode 15 out
    gpio write 15 1
    gpio mode 4 out
    gpio write 4 0
    python monitor.py
fi
