#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

# Functions
function Finish () {
    #	echo "done"
    echo "$CSV_DATE,$BATTERY,$SM_TEMP,$FD_TEMP,$INTERNAL_TEMP,$SMOKE_TEMP_LOW,$SMOKE_MID,$SMOKE_TEMP_HIGH,$KASA_STATE" >> "$CSV_FILE"
}

function LoadConfig () {
    local CONFIG_FILE="config.sh"
    if [ -f "$CONFIG_FILE" ]; then
        # shellcheck source=config.sh
        source "$CONFIG_FILE"
    else
        echo "Missing $CONFIG_FILE, exiting!"
        exit 1
    fi
}

function SetLEDState () {
    if [ "$#" -ne "2" ]; then
        echo "Wrong number of arguements to SetLEDState"
        echo "Expected 2, got $#"
        exit 1
    fi
    local COLOR="$1"
    local VALUE="$2"
    local ON_VAL="1"
    local OFF_VAL="0"
    local GPIO
    # TODO: Document pin hookups
    case "$COLOR" in
        "red")
            GPIO="4"
        ;;
        "green")
            GPIO="15"
            OFF_VAL="1"
            ON_VAL="0"
        ;;
        *)
            echo "bad value for led sent to SetLEDState"
            echo "expected \"red\" or \"green\", got \"$COLOR\""
            exit 1
        ;;
    esac
    case "$VALUE" in
        "on")
            gpio write "$GPIO" "$ON_VAL" &
        ;;
        "off")
            gpio write "$GPIO" "$OFF_VAL" &
        ;;
        *)
            echo "bad value for LED state sent to SetLEDState"
            echo "expected \"on\" or \"off\", got \"$VALUE\""
            exit 1
        ;;
    esac
    echo "Turning LED $COLOR $VALUE"
}

function SetKasaState() {
    local STATE
    local MSG
    if [ "$#" -eq "1" ]; then
        MSG="Turning hotplate $1"
    elif [ "$#" -eq "2" ]; then
        MSG="Turning hotplate $1 due to $2"
    else
        echo "Wrong number of arguements to SetKasaState"
        echo "Expected 1 or 2, got $#"
        exit 1
    fi
    STATE="$1"
    tplink-smarthome-api send "$TP_LINK_IP" '{"count_down":{"delete_all_rules":{}}}}'
    # NOTE: api commands must be blocking as they take a second or two
    # and another state update may come in
    case "$STATE" in
        "on")
            KASA_STATE="lightgreen"
            tplink-smarthome-api setPowerState "$TP_LINK_IP" true
            # Force off after 5 minutes if there's no commands
            tplink-smarthome-api send "$TP_LINK_IP" '{"count_down":{"add_rule":{"enable":1,"delay":300,"act":0,"name":"turn off"}}}'
        ;;
        "off")
            KASA_STATE="red"
            tplink-smarthome-api setPowerState "$TP_LINK_IP" false
        ;;
        *)
            echo "bad value for hotplate state sent to SetKasaState"
            echo "expected \"on\" or \"off\", got \"$STATE\""
            exit 1
        ;;
    esac
    echo "$MSG"
}

function WriteStages()
{
    #	echo "updating stages"
	cat > "$STAGE_FILE" <<EOL
#!/bin/bash
set -ue
STAGE=$STAGE
TIMESTAMP=$DATE_TS
EOL
    #	echo "reloading config"
    # Reload the config file with the new stage.
    LoadConfig
    #	echo "update complete"
}

# Define initial values for variables
LAST_BATTERY="0"
LAST_FD_TEMP="0"
LAST_SM_TEMP="0"
STAGE_TIME="0"
KASA_STATE=""
CSV_DATE=$(date -Iseconds)
DATE_TS=$(date +'%s')
STAGE_NAME="None"
STAGE_FILE="stage.sh"

# Load the configuration
LoadConfig

BATTERY="$1"
FD_TEMP="$2"
SM_TEMP="$3"

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
    SetLEDState "green" "on"
    
    # Play a sound
    omxplayer -o local /usr/lib/libreoffice/share/gallery/sounds/train.wav &
    
elif [ "$FD_TEMP" -ge "$INTERNAL_TEMP" ]; then
    #done
    SetLEDState "green" "on"
    
    # Play a sound
    omxplayer -o local /usr/lib/libreoffice/share/gallery/sounds/train.wav &
    
    if [ "$STAGE" -eq "0" ]; then
        # keep warm at target temp
        SMOKE_MID="$INTERNAL_TEMP"
    fi
else
    SetLEDState "green" "off"
fi

SMOKE_TEMP_HIGH=$((SMOKE_MID + 7))
SMOKE_TEMP_LOW=$((SMOKE_MID - 7))

if [ "$BATTERY" -le "$MIN_BATTERY" ] ; then
    #low battery
    SetLEDState "red" "on"
    
    # TODO: make this a function
    # Play a sound through the 3.5mm jack to indicate low battery
    omxplayer -o local /usr/lib/libreoffice/share/gallery/sounds/kling.wav &
else
    SetLEDState "red" "off"
fi

# Data for Highcharts
# order must mach startup.sh

#echo "writting state"
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
    # temp moving up too fast, disable the hotplate (trying to prevemt fires)
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
