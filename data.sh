#!/bin/bash
# FIXME: Read from config file
CSV_FILE=/var/www/html/current.csv
BAD_DATA=65536
SMOKE_MID=225
INTERNAL_TEMP=190
MIN_BATTERY=15
MAX_TEMP_CHANGE=2

BATTERY=$1
MT_TEMP=$2
SM_TEMP=$3

if [ $MT_TEMP -gt 180 ]; then
	SMOKE_MID=165
fi
SMOKE_TEMP_HIGH=`expr $SMOKE_MID + 3`
SMOKE_TEMP_LOW=`expr $SMOKE_MID - 3`

function SetLEDState () {
	if [ $# -ne 2 ]; then
		 echo "Wrong number of arguements to SetLEDState"
		 echo "Expected 2, got $#"
		 exit 1
	fi
	local COLOR=$1
	local VALUE=$2
	local ON_VAL=1
	local OFF_VAL=0
	local GPIO
	# TODO: Document pin hookups
	case "$COLOR" in
		"red")
			GPIO=4
		;;
		"green")
			GPIO=15
			OFF_VAL=1
			ON_VAL=0
		;;
		*)
			echo "bad value for led sent to SetLEDState"
			echo "expected \"red\" or \"green\", got \"$COLOR\""
			exit 1
		;;
	esac
	case "$VALUE" in
		"on")
			gpio write $GPIO $ON_VAL &
		;;
		"off")
			gpio write $GPIO $OFF_VAL &
		;;
		*)
			echo "bad value for LED state sent to SetLEDState"
			echo "expected \"on\" or \"off\", got \"$VALUE\""
			exit 1
		;;
	esac
	echo "Turning LED $COLOR $VALUE"
}


function SetKasaState()
{
	local STATE
	local MSG
	if [ $# -eq 1 ]; then
		MSG="Turning hotplate $1"
	elif [ $# -eq 2 ]; then
		MSG="Turning hotplate $1 due to $2"
	else
		 echo "Wrong number of arguements to SetKasaState"
		 echo "Expected 1 or 2, got $#"
		 exit 1
	fi
	STATE=$1
	
	# Is it possible to set this automatically?
	# FIXME: read from config file
	local TP_LINK_IP="192.168.0.1"

	# NOTE: api commands must be blocking as they take a second or two
	# and another state update may come in
	case "$STATE" in
		"on")
			tplink-smarthome-api setPowerState $TP_LINK_IP true
		;;
		"off")
			tplink-smarthome-api setPowerState $TP_LINK_IP false
		;;
		*)
			echo "bad value for hotplate state sent to SetKasaState"
			echo "expected \"on\" or \"off\", got \"$STATE\""
			exit 1
		;;
	esac
	echo "$MSG"
}


# Data for Highcharts
# order must mach startup.sh
echo -n "`date -Iseconds`," >> $CSV_FILE
if [ $BATTERY -le 100 ]; then
	echo -n $BATTERY >> $CSV_FILE
fi
echo -n "," >> $CSV_FILE
if [ $SM_TEMP -ne $BAD_DATA ]; then
	echo -n $SM_TEMP >> $CSV_FILE
fi
echo -n "," >> $CSV_FILE
if [ $MT_TEMP -ne $BAD_DATA ]; then
	echo -n $MT_TEMP >> $CSV_FILE
fi
echo "" >> $CSV_FILE
LAST_TEMP=0
if [ -f "last_temp.sh" ]; then
	source last_temp.sh
fi

if [ $BATTERY -le $MIN_BATTERY ] ; then
	#low battery
	SetLEDState "red" "on"
	
	# TODO: make this a function
	# Play a sound through the 3.5mm jack to indicate low battery
	omxplayer -o local /usr/lib/libreoffice/share/gallery/sounds/kling.wav &
else
	SetLEDState "red" "off"
fi
if [ $MT_TEMP -ge $INTERNAL_TEMP ]; then
	#done
	SetLEDState "green" "on"
	# turn off hot plate (at temp)
	SetKasaState "off" "internal temp meets or exceeds threshold ($MT_TEMP >= $INTERNAL_TEMP)"
	
	# Play a sound
	omxplayer -o local /usr/lib/libreoffice/share/gallery/sounds/train.wav &
else
	SetLEDState "green" "off"

	# only enable hotplate if the internal temp is below expected
	if [ "$SM_TEMP" -le "$SMOKE_TEMP_HIGH" ]; then
		# if the temp is dropping and we're less than or equal to the high value, start the hotplate
		if [ "$LAST_TEMP" -gt "$SMOKE_TEMP_HIGH" ]; then
			SetKasaState "on" "smoke temp meets or is below threshold ($SM_TEMP <= $SMOKE_TEMP_HIGH)"
		elif [ "$LAST_TEMP" -lt "$SM_TEMP" ]; then
			if [ $SM_TEMP -gt $SMOKE_TEMP_LOW ]; then
				SetKasaState "off" "smoke temp rising in band ($SMOKE_TEMP_LOW <= $SM_TEMP <= $SMOKE_TEMP_HIGH)"
			fi
		elif [ "$LAST_TEMP" -eq "$SM_TEMP" ]; then
			if [ "$SM_TEMP" -gt "$SMOKE_MID" ]; then
				SetKasaState "off" "smoke temp stable but above midpoint in band ($SMOKE_MID < $SM_TEMP <= $SMOKE_TEMP_HIGH)"
			elif [ "$SM_TEMP" -lt "$SMOKE_MID" ]; then
				SetKasaState "on" "smoke temp stable but below midpoint in band ($SMOKE_TEMP_LOW <= $SM_TEMP < $SMOKE_MID)"
			fi
		fi
	else
		#disable hotplate
		SetKasaState "off" "smoke temp meets or exceeds threshold ($SM_TEMP >= $SMOKE_TEMP_HIGH)"
	fi
	if [ $SM_TEMP -ge $SMOKE_TEMP_LOW ]; then
		# if the temp is rising and we're greater than or equal to the low value, stop the hotplate
		if [ $LAST_TEMP -lt $SMOKE_TEMP_LOW ] ; then
			SetKasaState "off" "smoke temp meets or exceeds threshold ($SM_TEMP >= $SMOKE_TEMP_LOW)"
		elif [ "$LAST_TEMP" -gt "$SM_TEMP" ]; then
			if [ $SM_TEMP -le $SMOKE_TEMP_HIGH ]; then
				SetKasaState "on" "smoke temp falling in band ($SMOKE_TEMP_LOW <= $SM_TEMP <= $SMOKE_TEMP_HIGH)"
			fi
		fi
	else
		#enable hotplate
		SetKasaState "on" "smoke temp meets or is below threshold ($SM_TEMP <= $SMOKE_TEMP_LOW)"
	fi

fi
if [ -f "last_temp.sh" ]; then
	source last_temp.sh
	DIFF=`expr $SM_TEMP - $LAST_TEMP`
	if [ $DIFF -gt $MAX_TEMP_CHANGE ] ; then
		# temp moving up too fast, disable the hotplate (trying to prevemt fires)
		SetKasaState "off" "smoke temp change meets or exceeds threshold ($DIFF >= $MAX_TEMP_CHANGE)"
	fi
fi
# TODO: Save more than just the last smoke temp
echo "#!/bin/bash" > last_temp.sh
echo "LAST_TEMP=$SM_TEMP" >> last_temp.sh
