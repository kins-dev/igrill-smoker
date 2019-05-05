#!/bin/bash
# Defining variables for other scripts
# shellcheck disable=2034
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}
IGRILL_CFG_DIR="${IGRILL_BAS_DIR}/config"
IGRILL_UTL_DIR="${IGRILL_BAS_DIR}/utils"
IGRILL_RUN_DIR="${IGRILL_BAS_DIR}/run"
