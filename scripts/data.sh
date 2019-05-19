#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

if [ -z "${IGRILL_BAS_DIR}" ]; then
    # https://stackoverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself
    SOURCE="${BASH_SOURCE[0]}"
    while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
    DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    done
    DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
    export IGRILL_BAS_DIR="${DIR}/.."
fi

# shellcheck source=utils/paths.sh
source "${IGRILL_BAS_DIR}/scripts/utils/paths.sh"

# pull in LED functions
# shellcheck source=utils/leds.sh
source "${IGRILL_UTL_DIR}/leds.sh"

# pull in sound functions
# shellcheck source=utils/sounds.sh
source "${IGRILL_UTL_DIR}/sounds.sh"

# pull in sound functions
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# shellcheck source=utils/kasa.sh
source "${IGRILL_UTL_DIR}/kasa.sh"

# Functions

# Used with trap to make sure the file is written before the script exits
function Finish () {
    # Data for Highcharts
    # order must mach startup.sh
    #	echo "done"

    if [ "mini" == "${iGrill__iGrill__Type}" ]
    then
        FD_TEMP=""
        INTERNAL_TEMP=""
    fi
    echo "$CSV_DATE,$BATTERY,$SM_TEMP,$FD_TEMP,$INTERNAL_TEMP,$SMOKE_TEMP_LOW,$SMOKE_MID,$SMOKE_TEMP_HIGH,$KASA_STATE" >> "$CSV_FILE"
}

# Load the config/user config/stages files
function LoadConfig () {
    local CONFIG_FILE="${IGRILL_SCR_DIR}/config.sh"
    if [ -f "$CONFIG_FILE" ]; then
        # shellcheck source=config.sh
        source "$CONFIG_FILE"
    else
        echo "Missing $CONFIG_FILE, exiting!"
        exit 1
    fi
}

# Should be moved out to another file


# Updates the stages (at a transition point)
function WriteStages()
{
    #	echo "updating stages"
	cat > "$STAGE_FILE" <<EOL
#!/bin/bash
# shellcheck disable=2034
true
# shellcheck disable=2086
set -\$-ue\${DEBUG+xv}
STAGE=$STAGE
TIMESTAMP=$DATE_TS
EOL
    # Reload the config file with the new stage.
    LoadConfig
}

# Define initial values for variables
LAST_BATTERY="0"
LAST_FD_TEMP="0"
LAST_SM_TEMP="0"
STAGE_TIME="0"
KASA_STATE=""
STAGE_NAME="None"
STAGE_FILE="stage.sh"
CSV_DATE=$(date -Iseconds)
DATE_TS=$(date +'%s')

# Load the configuration
LoadConfig

# TODO: check number of args
# TODO: Support iGrill mini / single probe setup
BATTERY="$1"
SM_TEMP="$2"
FD_TEMP="$3"

# If any of the values are bad, just load the previous data and go forward
if [ "$BATTERY" -eq "$BAD_DATA" ]; then
    BATTERY="$LAST_BATTERY"
fi
if [ "$SM_TEMP" -eq "$BAD_DATA" ]; then
    SM_TEMP="$LAST_SM_TEMP"
fi
if [ "$FD_TEMP" -eq "$BAD_DATA" ]; then
    FD_TEMP="$LAST_FD_TEMP"
fi

if [ "$TIMESTAMP" -gt "0" ]; then
    TIME_IN_S=$((DATE_TS - TIMESTAMP))
    STAGE_TIME=$((TIME_IN_S / 60))
fi

trap Finish EXIT


# Only if we're using stages
if [ "$STAGE" -gt "0" ]; then
    # if TIME is less than 0, then we're using temperature
    if [ "$TIME" -lt "0" ]; then
        if [ "$FD_TEMP" -ge "$INTERNAL_TEMP" ]; then
            STAGE=$((STAGE + 1))
            WriteStages
        fi
    else
        # Get the timestamp
        if [ "$TIMESTAMP" -eq "0" ]; then
            WriteStages
        else
            if [ "$STAGE_TIME" -ge "$TIME" ]; then
                STAGE=$((STAGE + 1))
                WriteStages
            fi
        fi
    fi
fi

if [ "$FD_DONE" -eq "1" ]; then
    #done
    LEDsSetState "green" "on"
    
    # Play a sound
    PlaySound "complete"
    
elif [ "$FD_TEMP" -ge "$INTERNAL_TEMP" ]; then
    #done
    LEDsSetState "green" "on"
    
    # Play a sound
    PlaySound "complete"
    
    if [ "$STAGE" -eq "0" ]; then
        # keep warm at target temp
        SMOKE_MID="$INTERNAL_TEMP"
    fi
else
    LEDsSetState "green" "off"
fi


SMOKE_TEMP_HIGH=$((SMOKE_MID + TEMP_SLOP))
SMOKE_TEMP_LOW=$((SMOKE_MID - TEMP_SLOP))

if [ "$BATTERY" -le "$MIN_BATTERY" ] ; then
    #low battery
    LEDsSetState "red" "on"
    PlaySound "low_battery"
else
    LEDsSetState "red" "off"
fi


#echo "writing state"
cat > "$STATE_FILE" <<EOL
[
  {
    "Stage":"$STAGE_NAME",
    "Battery":"$BATTERY",
    "Food Temp":"$FD_TEMP",
    "Target Food Temp":"$INTERNAL_TEMP",
    "Smoke Temp":"$SM_TEMP",
    "Smoke Target Temp":"$SMOKE_MID",
    "Smoke Target Low":"$SMOKE_TEMP_LOW",
    "Smoke Target High":"$SMOKE_TEMP_HIGH",
	"Stage Time":"$STAGE_TIME"
  }
]
EOL

# must write after config is reloaded
cat > "$LAST_TEMP_FILE" <<EOL
#!/bin/bash
set -ue
LAST_FD_TEMP=$FD_TEMP
LAST_SM_TEMP=$SM_TEMP
LAST_BATTERY=$BATTERY
EOL

#echo "Calculating diff expr $SM_TEMP - $LAST_SM_TEMP"
# Diff is used for rising/falling and to make sure it doesn't rise too fast
# if val is 0, expr returns non-zero exit code
set +e
DIFF=$((SM_TEMP - LAST_SM_TEMP))
if [ "$LAST_SM_TEMP" -eq "0" ]; then
    DIFF="0"
fi
#echo "$?"
set -e
#echo "finding direction"
# Direction is used to see if the smoke is above or below the target temp
DIRECTION="0"
if [ "$SM_TEMP" -gt "$SMOKE_MID" ]; then
    #	echo "temp high"
    DIRECTION="1"
    elif [ "$SM_TEMP" -lt "$SMOKE_MID" ]; then
    #	echo "temp low"
    DIRECTION="-1"
fi

# IN_BAND is used to see if the smoke is near the target temp, meaning finer grain controls to prevent ringing
IN_BAND="0"
if [ "$SM_TEMP" -ge "$SMOKE_TEMP_LOW" ]; then
    if [ "$SM_TEMP" -le "$SMOKE_TEMP_HIGH" ]; then
        #		echo "temp in band"
        IN_BAND="1"
    fi
fi

if [ "$DIFF" -gt "$MAX_TEMP_CHANGE" ] ; then
    # temp moving up too fast, disable the hotplate (trying to prevent fires)
    SetKasaState "off" "smoke temp change meets or exceeds threshold ($DIFF >= $MAX_TEMP_CHANGE)"
else
    #	echo "Temp change was $DIFF"
    if [ "$IN_BAND" -eq "0" ]; then
        echo "Out of band"
        if [ "$DIRECTION" -lt "0" ]; then
            #enable hotplate
            SetKasaState "on" "smoke temp is below threshold ($SM_TEMP < $SMOKE_TEMP_LOW)"
            elif [ "$DIRECTION" -gt "0" ]; then
            SetKasaState "off" "smoke temp is exceeds threshold ($SM_TEMP > $SMOKE_TEMP_HIGH)"
        else
            echo "Error, direction not set but out of band"
            exit 1
        fi
    else
        #		echo "in band"
        if [ "$DIFF" -eq "0" ]; then
            if [ "$DIRECTION" -lt "0" ]; then
                SetKasaState "on" "smoke temp stable but below midpoint in band ($SMOKE_TEMP_LOW <= $SM_TEMP < $SMOKE_MID)"
                elif [ "$DIRECTION" -gt "0" ]; then
                SetKasaState "off" "smoke temp stable but above midpoint in band ($SMOKE_MID < $SM_TEMP <= $SMOKE_TEMP_HIGH)"
            else
                echo "smoke temp stable and $SM_TEMP == $SMOKE_MID, doing nothing"
            fi
            elif [ "$DIFF" -gt "0" ]; then
            SetKasaState "off" "smoke temp rising in band ($SMOKE_TEMP_LOW <= $SM_TEMP <= $SMOKE_TEMP_HIGH) && ($LAST_SM_TEMP < $SM_TEMP)"
        else
            SetKasaState "on" "smoke temp falling in band ($SMOKE_TEMP_LOW <= $SM_TEMP <= $SMOKE_TEMP_HIGH) && ($LAST_SM_TEMP > $SM_TEMP)"
        fi
    fi
fi
