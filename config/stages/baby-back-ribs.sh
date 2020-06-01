#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# Defining variables for other scripts
# shellcheck disable=2034
:
# shellcheck disable=2154
set -$-ue${DEBUG+xv}

MINI_COMPATIBLE=true

case "${STAGE}" in
    1)
        # Warmup stage, keep plate at a cooler temp
        STAGE_NAME="Warmup"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        TIME=15
        ;;
    2)
        # Smoke stage, keep plate at cooler temp
        STAGE_NAME="Smoke"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        TIME=180
        ;;
    3)
        # Cook stage, move hotplate to higher temp
        STAGE_NAME="Cook"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        TIME=120
        ;;
    4)
        # Sauce stage
        STAGE_NAME="Sauce"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        TIME=60
        ;;
    5 | 6)
        # Keep warm stage, move hotplate to lower temp
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
