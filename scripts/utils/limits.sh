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
    IGRILL_BAS_DIR="$(readlink -f "${DIR}/../..")"
    export IGRILL_BAS_DIR
fi

# shellcheck source=paths.sh
source "${IGRILL_BAS_DIR}/scripts/utils/paths.sh"

function ResetLimits () {
    for i in $(seq 1 4); do
        local PROBE_NAME=LIMITS_Probe${i}
        eval "${PROBE_NAME}='[Probe${i}]'"
    done
}

function SetLimits () {
    local PROBE_NAME=LIMITS_Probe${1}
    local LOW
    local HIGH
    local CURRENT=$2
    local TARGET=$3
    local SLOP=$4
    if [ "${CURRENT}" -lt "${TARGET}" ]; then
        LOW=$((CURRENT - SLOP))
        HIGH=$((TARGET + SLOP))
    else
        LOW=$((TARGET - SLOP))
        HIGH=$((CURRENT + SLOP))
    fi
    VAL="[Probe${1}]
LOW_TEMP=${LOW}
HIGH_TEMP=${HIGH}"
    eval "${PROBE_NAME}=\${VAL}"
}

function PrintLimits () {
    echo "[DEFAULT]
LOW_TEMP=-32768
HIGH_TEMP=32767
"

    for i in $(seq 1 4); do
        local PROBE_NAME=LIMITS_Probe${i}
        eval "VAL=\${${PROBE_NAME}}"
        echo "$VAL"
        echo ""
    done
}

function WriteLimits () {
    
}
