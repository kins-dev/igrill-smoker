#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# Defining variables for other scripts
# shellcheck source-path=SCRIPTDIR/tests/scripts
:
# shellcheck disable=2154
set -$-ue${DEBUG+xv}

function ResetLimits()
{
    for i in $(seq 1 4); do
        local PROBE_NAME=LIMITS_Probe${i}
        eval "${PROBE_NAME}='[Probe${i}]'"
    done
}

function SetLimits()
{
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

function PrintLimits()
{
    echo "[DEFAULT]
LOW_TEMP=-32768
HIGH_TEMP=32767
"

    for i in $(seq 1 4); do
        local PROBE_NAME=LIMITS_Probe${i}
        eval "VAL=\${${PROBE_NAME}}"
        echo "${VAL}"
        echo ""
    done
}

ResetLimits
SetLimits 1 65 120 5
SetLimits 2 130 100 10
PrintLimits
