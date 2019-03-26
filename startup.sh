#!/bin/bash
WEBDIR="/var/www/html"
if ! [ -f /tmp/igrill.json ] ; then
    FILE="$WEBDIR/$(date +"%Y_%m_%d_%I_%M_%p").csv"
    sudo touch $FILE
    sudo chmod a+rw $FILE
    echo "Time,Battery,Smoke Temp,Meat Temp" > $FILE
    sudo rm -f $WEBDIR/current.csv
    sudo ln -s $FILE $WEBDIR/current.csv
    sudo bash gen_json.sh
    rm -f max_meat_temp.sh
    gpio mode 15 out
    gpio write 15 1
    gpio mode 4 out
    gpio write 4 0
    python monitor.py
fi
