#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

# https://stackoverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

IGRILL_BAS_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
export IGRILL_BAS_DIR
pushd "${IGRILL_BAS_DIR}"
source "scripts/utils/paths.sh"

if ! [ -f "$IGRILL_CFG_DIR/iGrill_config.ini" ]; then
    echo "Error: $IGRILL_CFG_DIR/iGrill_config.ini mot found"
    echo "Please setup the ini file based on the example"
    exit 1
fi

# shellcheck source=scripts/utils/bt.sh
source "${IGRILL_UTL_DIR}/bt.sh"
# shellcheck source=scripts/utils/leds.sh
source "${IGRILL_UTL_DIR}/leds.sh"

function finish  () {
    # Cleanup on exit
    pushd "${IGRILL_RUN_DIR}"
    rm -f igrill.json
    rm -f last_temp.sh
    rm -f stage.sh
    popd
    popd
}

# shellcheck source=scripts/config.sh
source "${IGRILL_SCR_DIR}/config.sh"

WEBDIR="${iGrill__Reporting__ResultsDirectory}"

if ! [ -f "${IGRILL_RUN_DIR}/igrill.json" ] ; then
    # Setup CSV file
    FILE="$WEBDIR/$(date +"%Y_%m_%d_%I_%M_%p").csv"
    sudo touch "$FILE"
    sudo chmod a+rw "$FILE"
    echo "Time,Battery,Smoke Temp,Food Temp,Internal Target,Smoke Target Low,Smoke Target,Smoke Target High,Plug State" > "$FILE"
    
    # Link CSV file
    sudo rm -f "$CSV_FILE"
    sudo ln -s "$FILE" "$CSV_FILE"
    
    # Setup state file
    sudo touch "$STATE_FILE"
    sudo chmod a+rw "$STATE_FILE"
    sudo "${IGRILL_UTL_DIR}/gen_json.sh"
    
    # Cleanup from last run (shouldn't be needed)
    pushd "${IGRILL_RUN_DIR}"
    rm -f last_temp.sh
    rm -f stage.sh
    popd

    trap finish INT
    trap finish EXIT
    if [ ! -f "${IGRILL_SCR_DIR}/py_config/mac_config.py" ]; then
        "${IGRILL_UTL_DIR}/get_mac.sh"
    fi
    
    LEDsReset

    # deal with unexpected wireless issues
    while true; do
        # reset the bluetooth connection
        BtReset

        # python may fail if disconnected
        set +e
        python3 "${IGRILL_SCR_DIR}/monitor.py"
        set -e
    done
fi