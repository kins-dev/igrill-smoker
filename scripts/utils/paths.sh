#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# Defining variables for other scripts
# shellcheck disable=2034
# shellcheck source-path=SCRIPTDIR/scripts/utils
:
# shellcheck disable=2154
set -$-ue${DEBUG+xv}

VALUE=${IGRILL_BAS_DIR:-}
if [ -z "${VALUE}" ]; then
    # https://stackoverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself
    SOURCE="${BASH_SOURCE[0]}"
    while [ -h "${SOURCE}" ]; do # resolve $SOURCE until the file is no longer a symlink
        DIR="$(cd -P "$(dirname "${SOURCE}")" > /dev/null 2>&1 && pwd)"
        SOURCE="$(readlink "${SOURCE}")"
        [[ ${SOURCE} != /* ]] && SOURCE="${DIR}/${SOURCE}" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    done
    DIR="$( cd -P "$( dirname "${SOURCE}")"  > /dev/null 2>&1 && pwd)"
    IGRILL_BAS_DIR="$(readlink -f "${DIR}/../..")"
    export IGRILL_BAS_DIR
fi

export IGRILL_CFG_DIR="${IGRILL_BAS_DIR}/config"
export IGRILL_SCR_DIR="${IGRILL_BAS_DIR}/scripts"
export IGRILL_PYC_DIR="${IGRILL_SCR_DIR}/pygrill/config"
export IGRILL_UTL_DIR="${IGRILL_SCR_DIR}/utils"
export IGRILL_RUN_DIR="${IGRILL_BAS_DIR}/run"
