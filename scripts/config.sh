#!/bin/bash
# Defining variables for other scripts
# shellcheck disable=2034
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
# shellcheck source=utils/read_ini.sh
source "${IGRILL_UTL_DIR}/read_ini.sh"

if [ -f "$IGRILL_CFG_DIR/iGrill_config.ini" ]; then
    read_ini "$IGRILL_CFG_DIR/iGrill_config.ini" --prefix "iGrill"
else
    echo "Error $IGRILL_CFG_DIR/iGrill_config.ini does not exist, please read the setup instructions"
fi

CSV_FILE=/var/www/html/current.csv
STATE_FILE=/var/www/html/state.json
BAD_DATA=-2000
TIME=-1
TIMESTAMP=0
FOOD=brisket
TEMP_SLOP=7
# Used to warn on low battery
MIN_BATTERY=15
# overridden by user-config.sh
TP_LINK_IP="192.168.0.1"
STAGE_NAME="Unknown"
# Set to 1 to use stages
STAGE=0
SMOKE_MID=225
INTERNAL_TEMP=190
MAX_TEMP_CHANGE=2
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

# allow user overrides
if [ -f "${USER_CFG}" ]; then
    # shellcheck source=../config/user-config.example.sh
    source "${USER_CFG}"
fi

if [ -f "${IGRILL_CFG_DIR}/stages/${FOOD}.sh" ]; then
    if [ $STAGE -eq 0 ]; then
        STAGE=1
    fi
    # shellcheck source=../config/stages/brisket.sh
    # shellcheck source=../config/stages/pork-shoulder.sh
    # shellcheck source=../config/stages/baby-back-ribs.sh
    source "${IGRILL_CFG_DIR}/stages/${FOOD}.sh"
fi
