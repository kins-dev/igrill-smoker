#!/bin/bash
if ! [ -f /tmp/data.csv ] ; then
    echo "Time,Battery,Smoke Temp,Meat Temp" > /tmp/data.csv
    gpio mode 15 out
    gpio write 15 1
    gpio mode 4 out
    gpio write 4 0
    python monitor.py
fi