#!/bin/bash
# Defining variables for other scripts
# shellcheck disable=2034
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

MINI_COMPATIBLE=false

# Note: for this to work. Internal temp must be increased at each stage
# the system will go to the next stage when the food hits the designated
# internal temp

case "$STAGE" in
    1)
        # Warmup stage, keep plate at a cooler temp and limit temp rise
        STAGE_NAME="Warmup"
        SMOKE_MID=250
        MAX_TEMP_CHANGE=1
        INTERNAL_TEMP=50
    ;;
    2)
        # Slow cook stage
        STAGE_NAME="Slow Cook"
        SMOKE_MID=250
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=110
    ;;
    3)
        # Cook stage, move hotplate to higher temp, allow bigger temp rise
        STAGE_NAME="Crust"
        SMOKE_MID=400
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=135
    ;;
    4|5)
        # Keep warm stage allow bigger temp rise
        STAGE_NAME="Keep warm"
        SMOKE_MID=135
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=190
        # signal we're done
        FD_DONE=1
        # Stay in this stage
        STAGE=4
    ;;
    *)
        echo "error: unknown stage"
        exit 1
    ;;
esac
