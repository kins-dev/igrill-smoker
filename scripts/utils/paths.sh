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
export IGRILL_CFG_DIR="${IGRILL_BAS_DIR}/config"
export IGRILL_SCR_DIR="${IGRILL_BAS_DIR}/scripts"
export IGRILL_PYC_DIR="${IGRILL_SCR_DIR}/pygrill/config"
export IGRILL_UTL_DIR="${IGRILL_SCR_DIR}/utils"
export IGRILL_RUN_DIR="${IGRILL_BAS_DIR}/run"
