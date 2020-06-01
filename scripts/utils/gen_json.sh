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

# shellcheck source=../config.sh
source "${IGRILL_SCR_DIR}/config.sh"

WEBDIR="${iGrill__Reporting__ResultsDirectory}"

# TODO: Move to ini file
OUTFILE="${WEBDIR}/items.json"
echo "[" > "${OUTFILE}"
ADD_COMMA=0
pushd "${WEBDIR}"
# need items in a specific order so I cannot use globs
# shellcheck disable=2045
for file in $(ls -t -1 [0-9]*.csv); do
    if [ "${ADD_COMMA}" -ne "0" ]; then
        echo "," >> "${OUTFILE}"
    fi
    ADD_COMMA=1
    echo "{\"name\":\"${file}\"}" >> "${OUTFILE}"
done
popd
echo "]" >> "${OUTFILE}"
