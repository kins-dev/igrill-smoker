#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# shellcheck source-path=SCRIPTDIR/tests/scripts
:
# shellcheck disable=2154
set -$-ue${DEBUG+xv}

source "../../scripts/utils/base_dir.sh"
echo "${IGRILL_BAS_DIR}"
