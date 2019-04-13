#!/bin/bash
set -$-ue${DEBUG+xv}
WEBDIR="/var/www/html"
OUTFILE="$WEBDIR/items.json"
echo "[" > $OUTFILE
ADD_COMMA=0
for file in $(ls -t -1 $WEBDIR | grep "\.csv$" | grep "^[0-9]")
#for file in $(ls -t -1 $WEBDIR | grep "\.csv$")
do
    if [ $ADD_COMMA -ne "0" ]; then
        echo "," >> $OUTFILE
    fi
    ADD_COMMA=1
    echo "{\"name\":\"$file\"}" >> $OUTFILE
done
echo "]" >> $OUTFILE
