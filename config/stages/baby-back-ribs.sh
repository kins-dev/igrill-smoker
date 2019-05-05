#!/bin/bash
# Defining variables for other scripts
# shellcheck disable=2034
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

# Note: for this to work. Internal temp must be increased at each stage
# the system will go to the next stage when the food hits the desgiated
# internal temp

case "$STAGE" in
    1)
        # Warmup stage, keep plate at a cooler temp and limit temp rise
        STAGE_NAME="Warmup"
        SMOKE_MID=180
        MAX_TEMP_CHANGE=1
        TIME=15
    ;;
    2)
        # Smoke stage, keep plate at cooler temp, but allow bigger temp rise
        STAGE_NAME="Smoke"
        SMOKE_MID=180
        MAX_TEMP_CHANGE=2
        TIME=180
    ;;
    3)
        # Braise stage, move hotplate to higher temp, allow bigger temp rise
        STAGE_NAME="Braise"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        TIME=120
    ;;
    4)
        # Sauce stage, move hotplate to higher temp, allow bigger temp rise
        STAGE_NAME="Sauce"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        TIME=60
    ;;
    5|6)
        # Keep warm stage, move hotplate to higher temp, allow bigger temp rise
        STAGE_NAME="Keep warm"
        SMOKE_MID=165
        MAX_TEMP_CHANGE=2
        TIME=100
        # signal we're done
        FD_DONE=1
        # Stay in this stage
        STAGE=5
    ;;
    *)
        echo "error: unknown stage"
        exit 1
    ;;
esac