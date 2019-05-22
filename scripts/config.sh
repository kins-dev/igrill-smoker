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

# shellcheck source=utils/read_ini.sh
source "${IGRILL_UTL_DIR}/read_ini.sh"

# shellcheck source=utils/defaults.sh
source "${IGRILL_UTL_DIR}/defaults.sh"

if [ -f "$IGRILL_CFG_DIR/iGrill_config.ini" ]; then
    read_ini "$IGRILL_CFG_DIR/iGrill_config.ini" --prefix "iGrill"
fi
RESULTS_DIRECTORY="${iGrill__Reporting__ResultsDirectory}"

CSV_FILE="${RESULTS_DIRECTORY}/${iGrill__Reporting__CSVFile}"
STATE_FILE="${RESULTS_DIRECTORY}/${iGrill__Reporting__StateFile}"
BAD_DATA=-2000
TIME=-1
TIMESTAMP=0
FOOD="${iGrill__Smoking__Food}"
TEMP_SLOP="${iGrill__Smoking__TempBandSize}"
# Used to warn on low battery
MIN_BATTERY=15
# overridden by user-config.sh
TP_LINK_IP="${iGrill__TPLink__IP}"
STAGE_NAME="Unknown"
# Set to 1 to use stages
STAGE=0
SMOKE_MID="${iGrill__Smoking__SmokeMid}"
INTERNAL_TEMP="${iGrill__Smoking__InternalTarget}"
MAX_TEMP_CHANGE="${iGrill__Smoking__MaxTempChange}"
FD_DONE=0
STAGE_FILE="${IGRILL_RUN_DIR}/stage.sh"
LAST_TEMP_FILE="${IGRILL_RUN_DIR}/last_temp.sh"
USER_CFG="${IGRILL_CFG_DIR}/user-config.sh"
LAST_SM_TEMP=0
LAST_FD_TEMP=0

if [ -f "${STAGE_FILE}" ]; then
    # shellcheck source=../run/stage.sh
    source "${STAGE_FILE}"
fi

if [ -f "${LAST_TEMP_FILE}" ]; then
    # shellcheck source=../run/last_temp.sh
    source "${LAST_TEMP_FILE}"
fi

if [ "Mini" == "${iGrill__iGrill__Type}" ]
then
    if ! [ "0" == "${iGrill__Probes__FoodProbe}" ]
    then
        echo "Error: Using an iGrill mini means food probe must be set to 0 in iGrill_config.ini"
        exit 1
    fi
    if ! [ "1" == "${iGrill__Probes__SmokeProbe}" ]
    then
        echo "Error: Using an iGrill mini means smoke probe must be set to 1 in iGrill_config.ini"
        exit 1
    fi
fi

# Make sure probe values are within expected ranges
if [ "0" -gt "${iGrill__Probes__FoodProbe}" ] || [ "4" -lt "${iGrill__Probes__FoodProbe}" ]
then
    echo "Error: Food probe must be set between 0 and 4 in iGrill_config.ini"
    exit 1
fi
if [ "1" -gt "${iGrill__Probes__SmokeProbe}" ] || [ "4" -lt "${iGrill__Probes__SmokeProbe}" ]
then
    echo "Error: Smoke probe must be set between 0 and 4 in iGrill_config.ini"
    exit 1
fi
if [ "${iGrill__Probes__FoodProbe}" == "${iGrill__Probes__SmokeProbe}" ]
then
    echo "Error: Smoke probe must be set to a different value than the food probe iGrill_config.ini"
    exit 1
fi

if [ -f "${IGRILL_CFG_DIR}/stages/${FOOD}.sh" ]; then
    if [ $STAGE -eq 0 ]; then
        STAGE=1
    fi
    # shellcheck source=../config/stages/brisket.sh
    # shellcheck source=../config/stages/pork-shoulder.sh
    # shellcheck source=../config/stages/baby-back-ribs.sh
    source "${IGRILL_CFG_DIR}/stages/${FOOD}.sh"

    if [ "0" == "${iGrill__Probes__FoodProbe}" ]
    then
        if ! [ true == "${MINI_COMPATIBLE}" ]
        then
            echo "Error: Using a stage that is incompatible with the food probe disabled"
            exit 1
        fi
    fi
else
    if ! [ "None" == "${FOOD}" ]
    then
        echo "Error: Unknown stage file \"${FOOD}\", did you mean None?"
        exit 1
    fi
fi
