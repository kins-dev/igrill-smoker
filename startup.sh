#!/bin/bash
if ! [ -f /tmp/igrill.json ] ; then
    FILE="$(date +"%Y_%m_%d_%I_%M_%p").csv"
    sudo touch /var/www/html/$FILE
    sudo chmod a+rw /var/www/html/$FILE
    echo "Time,Battery,Smoke Temp,Meat Temp" > /var/www/html/$FILE
    sudo rm -f /var/www/html/current.csv
    sudo ln -s /var/www/html/$FILE /var/www/html/current.csv
    gpio mode 15 out
    gpio write 15 1
    gpio mode 4 out
    gpio write 4 0
    python monitor.py
fi
