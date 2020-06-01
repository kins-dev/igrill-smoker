#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# shellcheck source-path=SCRIPTDIR/scripts/utils
:
# shellcheck disable=2154
set -$-ue${DEBUG+xv}

# Script to detect the attached board and the revision
