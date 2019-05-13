#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
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
        SMOKE_MID=180
        MAX_TEMP_CHANGE=1
        INTERNAL_TEMP=70
    ;;
    2)
        # Smoke stage, keep plate at cooler temp, but allow bigger temp rise
        STAGE_NAME="Smoke"
        SMOKE_MID=180
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=120
    ;;
    3)
        # Cook stage, move hotplate to higher temp, allow bigger temp rise
        STAGE_NAME="Cook"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=170
    ;;
    4)
        # Braise stage, move hotplate to higher temp, allow bigger temp rise
        STAGE_NAME="Braise"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=185
    ;;
    5|6)
        # Keep warm stage, move hotplate to higher temp, allow bigger temp rise
        STAGE_NAME="Keep warm"
        SMOKE_MID=160
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=190
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