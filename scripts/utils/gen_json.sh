#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}
WEBDIR="/var/www/html"
OUTFILE="$WEBDIR/items.json"
echo "[" > $OUTFILE
ADD_COMMA=0
pushd "$WEBDIR"
# need items in a specific order so I cannot use globs
# shellcheck disable=2045
for file in $(ls -t -1 [0-9]*.csv)
do
    if [ $ADD_COMMA -ne "0" ]; then
        echo "," >> $OUTFILE
    fi
    ADD_COMMA=1
    echo "{\"name\":\"$file\"}" >> $OUTFILE
done
popd
echo "]" >> $OUTFILE
