#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# shellcheck disable=2034
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

function SetKasaState() {
    local STATE
    local MSG
    if [ "$#" -eq "1" ]; then
        MSG="Turning hotplate $1"
    elif [ "$#" -eq "2" ]; then
        MSG="Turning hotplate $1 due to $2"
    else
        echo "Wrong number of arguments to SetKasaState"
        echo "Expected 1 or 2, got $#"
        exit 1
    fi
    STATE="$1"
    tplink-smarthome-api send "$TP_LINK_IP" '{"count_down":{"delete_all_rules":{}}}}'
    
    # NOTE: api commands must be blocking as they take a second or two
    # and another state update may come in
    case "$STATE" in
        "on")
            # TODO: Move kasa state to something that can be queried at write time
            KASA_STATE="lightgreen"
            tplink-smarthome-api setPowerState "$TP_LINK_IP" true
            # Force off after 5 minutes if there's no commands
            tplink-smarthome-api send "$TP_LINK_IP" '{"count_down":{"add_rule":{"enable":1,"delay":300,"act":0,"name":"turn off"}}}'
        ;;
        "off")
            KASA_STATE="red"
            tplink-smarthome-api setPowerState "$TP_LINK_IP" false
        ;;
        *)
            echo "bad value for hotplate state sent to SetKasaState"
            echo "expected \"on\" or \"off\", got \"$STATE\""
            exit 1
        ;;
    esac
    echo "$MSG"
}

function GetKasaIP() {
    if ! [ "$#" -eq "1" ]; then
        echo "Wrong number of arguments to GetKasaIp"
        echo "Expected 1, got $#"
        exit 1
    fi
    local NAME=$1
    coproc stdbuf -oL tplink-smarthome-api search
    while read -r LINE; do

        # when we find the iGrill_V2 setup that information
        if [[ "${LINE}" = *"${NAME}" ]]; then
            TP_LINK_IP="$(echo "${LINE}" | cut -d " " -f 4)"
            break
        fi
    done <&"${COPROC[0]}"
    kill "${COPROC_PID}"
    export TP_LINK_IP
}