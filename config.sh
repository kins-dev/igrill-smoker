#!/bin/bash
# Defining variables for other scripts
# shellcheck disable=2034
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}
CSV_FILE=/var/www/html/current.csv
STATE_FILE=/var/www/html/state.json
BAD_DATA=63536
TIME=-1
TIMESTAMP=0
FOOD=brisket
# Used to warn on low battery
MIN_BATTERY=15
TP_LINK_IP="192.168.0.1"

STAGE_NAME="Unknown"
# Set to 1 to use stages
STAGE=0
SMOKE_MID=225
INTERNAL_TEMP=190
MAX_TEMP_CHANGE=2
FD_DONE=0
STAGE_FILE="stage.sh"

if [ -f "$STAGE_FILE" ]; then
    # shellcheck source=stage.sh
    source "$STAGE_FILE"
fi

LAST_SM_TEMP=0
LAST_FD_TEMP=0

if [ -f "last_temp.sh" ]; then
    # shellcheck source=last_temp.sh
    source last_temp.sh
fi

# allow user overrides
if [ -f "user-config.sh" ]; then
    # shellcheck source=user-config.sh
    source "user-config.sh"
fi

if [ -f "stages/${FOOD}.sh" ]; then
    if [ $STAGE -eq 0 ]; then
        STAGE=1
    fi
    # shellcheck source=stages/brisket.sh
    # shellcheck source=stages/pork-shoulder.sh
    # shellcheck source=stages/baby-back-ribs.sh
    source "stages/${FOOD}.sh"
fi
