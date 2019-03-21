#!/bin/bash
if ! [ -f /tmp/data.csv ] ; then
    # FIXME: Build graph based on data
    echo "Time,Battery,Meat Temp,Smoke Temp" > /tmp/data.csv
    gpio mode 15 out
    gpio write 15 1
    gpio mode 4 out
    gpio write 4 0
    # FIXME: see if we cam run as the user
    sudo python monitor.py
fi