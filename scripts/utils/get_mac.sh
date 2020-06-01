#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
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

# shellcheck source=paths.sh
source "${IGRILL_BAS_DIR}/scripts/utils/paths.sh"
# shellcheck source=bt.sh
source "${IGRILL_UTL_DIR}/bt.sh"

OUTPUT="${IGRILL_PYC_DIR}/mac_config.py"

echo "Turn on your iGrill now"

BtReset

# stdbuf is needed to prevent buffering of lines
# by hcitool
coproc sudo stdbuf -oL hcitool lescan

while read -r CMD; do

    # when we find the iGrill_V2 setup that information
    if [[ ${CMD} = *"iGrill"* ]]; then
        MAC=${CMD:0:17}
        echo "${MAC}"
        echo -n "ADDRESS='" > "${OUTPUT}"
        echo -n "${MAC}" >> "${OUTPUT}"
        echo "'" >> "${OUTPUT}"
        break
    fi
done <&"${COPROC[0]}"

# This will forcibly kill the scan
BtReset
