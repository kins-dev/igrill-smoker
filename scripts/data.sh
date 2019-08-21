#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

if ! [ "$#" -eq "3" ]; then
    echo "Wrong number of arguments to data.sh"
    echo "Expected 3, got $#"
    exit 1
fi

VALUE=${IGRILL_BAS_DIR:-}
if [ -z "${VALUE}" ]; then
    # https://stackoverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself
    SOURCE="${BASH_SOURCE[0]}"
    while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
        DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
        SOURCE="$(readlink "$SOURCE")"
        [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    done
    DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
    IGRILL_BAS_DIR="$(readlink -f "${DIR}/..")"
    export IGRILL_BAS_DIR
fi

# shellcheck source=utils/paths.sh
source "${IGRILL_BAS_DIR}/scripts/utils/paths.sh"

# pull in limit functions
# shellcheck source=utils/limits.sh
source "${IGRILL_UTL_DIR}/limits.sh"

# Functions

# Used with trap to make sure the file is written before the script exits
function Finish () {
    # Data for Highcharts
    # order must mach startup.sh
    #	echo "done"
    local KASA_STATE="red"
    local KASA_PLUG_STATE
    local SSR_STATE
    SSR_STATE=$(PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --status)
    KASA_PLUG_STATE=$(PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.kasa.kasa_client --status)
    if [ "on" == "$KASA_PLUG_STATE" ]; then
        KASA_STATE="lightgreen"
    fi
    if [ "0" == "${iGrill__Probes__FoodProbe}" ]; then
        FD_TEMP=""
        INTERNAL_TEMP=""
    fi
    echo "$CSV_DATE,$BATTERY,$SM_TEMP,$FD_TEMP,$INTERNAL_TEMP,$SMOKE_TEMP_LOW,$SMOKE_MID,$SMOKE_TEMP_HIGH,$KASA_STATE,$SSR_STATE" >> "$CSV_FILE"
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


# Updates the stages (at a transition point)
function WriteStages()
{
    ResetLimits
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
    if ! [ "0" == "${iGrill__Probes__FoodProbe}" ]; then
        SetLimits "${iGrill__Probes__FoodProbe}" "$FD_TEMP" "$INTERNAL_TEMP" 5
    fi
    SetLimits "${iGrill__Probes__SmokeProbe}" "$SM_TEMP" "$SMOKE_MID" 20
    
    WriteLimits
    
    # Reload the config file with the new stage.
    LoadConfig
}

# Define initial values for variables
LAST_BATTERY="0"
LAST_FD_TEMP="0"
LAST_SM_TEMP="0"
STAGE_TIME="0"
STAGE_NAME="None"
STAGE_FILE="stage.sh"
CSV_DATE=$(date -Iseconds)
DATE_TS=$(date +'%s')

# Load the configuration
LoadConfig

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
        elif [ "$STAGE_TIME" -ge "$TIME" ]; then
                STAGE=$((STAGE + 1))
                WriteStages
        fi
    fi
fi

SMOKING_COMPLETE=""
LOW_BATTERY=""
if [ "$FD_DONE" -eq "1" ]; then
    #done
    SMOKING_COMPLETE="--done"
    
elif [ "$FD_TEMP" -ge "$INTERNAL_TEMP" ]; then
    SMOKING_COMPLETE="--done"
    
    if [ "$STAGE" -eq "0" ]; then
        # keep warm at target temp
        SMOKE_MID="$INTERNAL_TEMP"
    fi
fi


SMOKE_TEMP_HIGH=$((SMOKE_MID + TEMP_SLOP))
SMOKE_TEMP_LOW=$((SMOKE_MID - TEMP_SLOP))

if [ "$BATTERY" -le "$MIN_BATTERY" ] ; then
    #low battery
    LOW_BATTERY="--low_battery"
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
#echo "DIRECTION=${DIRECTION}"
#echo "IN_BAND=${IN_BAND}"
#echo "DIFF=${DIFF}"
if [ "${DIRECTION}" -lt "0" ]; then # colder than target
    if [ "${IN_BAND}" -eq "0" ]; then
        if [ "${DIFF}" -lt "0" ]; then
            PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --cold
        elif [ "${DIFF}" -gt "${MAX_TEMP_CHANGE}" ]; then
            PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --hot
        else
            MAX_TEMP_CHANGE_MID=$((MAX_TEMP_CHANGE / 2))
            if [ "${DIFF}" -lt "${MAX_TEMP_CHANGE_MID}" ]; then
                PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band --cold
            elif [ "${DIFF}" -gt "${MAX_TEMP_CHANGE_MID}" ]; then
                PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band --hot
            else
                PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band
            fi
        fi
        PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --cold ${SMOKING_COMPLETE} ${LOW_BATTERY}
    else
        PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --cool ${SMOKING_COMPLETE} ${LOW_BATTERY}
        if [ "${DIFF}" -eq "0" ]; then # steady
            PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band --cold
        elif [ "${DIFF}" -gt "0" ]; then # rising
            PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band --hot
        else
            PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band --cold
        fi
    fi
elif [ "${DIRECTION}" -gt "0" ]; then
    if [ "${IN_BAND}" -eq "0" ]; then
        #echo "above target, out of band"
        PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --hot
        PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --hot ${SMOKING_COMPLETE} ${LOW_BATTERY}
    else
        #echo "above target, in band"
        if [ "${DIFF}" -eq "0" ]; then # steady
            PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band
        elif [ "${DIFF}" -gt "0" ]; then # rising
            PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band --hot
        else
            PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band --cold
        fi
        PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --warm ${SMOKING_COMPLETE} ${LOW_BATTERY}
    fi
else
    if [ "${DIFF}" -eq "0" ]; then # steady
        PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band
    elif [ "${DIFF}" -gt "0" ]; then # rising
        PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band --hot
    else
        PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.ssrc_client --in_band --cold
    fi
    PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.leds --perfect ${SMOKING_COMPLETE} ${LOW_BATTERY}
fi
PYTHONPATH="${IGRILL_SCR_DIR}" python3 -m pygrill.board.buzzer_client ${SMOKING_COMPLETE} ${LOW_BATTERY}