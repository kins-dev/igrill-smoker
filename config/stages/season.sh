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
        STAGE_NAME="Season"
        SMOKE_MID=235
        MAX_TEMP_CHANGE=20
        TIME=120
    ;;
    2|3)
        STAGE_NAME="Done"
        SMOKE_MID=0
        MAX_TEMP_CHANGE=20
        TIME=100
        # signal we're done
        FD_DONE=1
        # Stay in this stage
        STAGE=2

    ;;
    *)
        echo "error: unknown stage"
        exit 1
    ;;
esac