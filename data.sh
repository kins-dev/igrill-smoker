#!/bin/bash

# TODO:
# 	Add stages
# 	Reorder data
# 	Deal with missing values
#	Set -ue
# 	Alter polling time
#	Save plug state in data

SMOKE_MID=225
SMOKE_TEMP_HIGH=`expr $SMOKE_MID + 3`
SMOKE_TEMP_LOW=`expr $SMOKE_MID - 3`

INTERNAL_TEMP=185
MIN_BATTERY=15

# Is it possible to set this automatically?
TP_LINK_IP="192.168.0.1"

# Data for Highcharts
echo "`date -Iseconds`,$1,$2,$3" >> /tmp/data.csv

if [ $1 -lt $MIN_BATTERY ] ; then
	#low battery
	gpio write 4 1 &
	omxplayer -o local /usr/lib/libreoffice/share/gallery/sounds/kling.wav &
else
	gpio write 4 0 &
fi
if [ $2 -ge $INTERNAL_TEMP ]; then
	#done
	gpio write 15 0 &
	# turn off hot plate (at temp)
	echo "turning off hotplate due to internal temp"
	tplink-smarthome-api setPowerState $TP_LINK_IP false
	#omxplayer -o local /usr/lib/libreoffice/share/gallery/sounds/train.wav &
else
	gpio write 15 1 &
	# only enable hotplate if the internal temp is below expected
	if [ $3 -ge $SMOKE_TEMP_HIGH ]; then
		#disable hotplate
		echo "Turning off hotplate due to temp"
		tplink-smarthome-api setPowerState $TP_LINK_IP false
	fi
	if [ $3 -le $SMOKE_TEMP_LOW ]; then
		#enable hotplate
		echo "Turning on hotplate due to temp"
		tplink-smarthome-api setPowerState $TP_LINK_IP true
	fi

fi
source last_temp.sh
DIFF=`expr $3 - $LAST_TEMP`
if [ $DIFF -ge 2 ] ; then
	# temp moving up too fast, disable the hotplate
	echo "temp change is too high, turning off hot plate"
	tplink-smarthome-api setPowerState $TP_LINK_IP false
fi


echo "#!/bin/bash" > last_temp.sh
echo "LAST_TEMP=$3" >> last_temp.sh

