#!/bin/bash
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