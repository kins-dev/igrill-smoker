# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
KASA_DAEMON_NET_BUFFER_SIZE                 = 2048
KASA_DAEMON_NET_HEADER_SIZE                 = 4
KASA_DAEMON_NET_DISCOVER_IP                 = "255.255.255.255"
KASA_DAEMON_NET_PORT                        = 9999

KASA_DAEMON_PYRO_HOST                       ="localhost"
KASA_DAEMON_PYRO_PORT                       = 9998
KASA_DAEMON_PYRO_OBJECT_ID                  = "Kasa"

KASA_DAEMON_JSON_DISCOVER                   = b'{"system":{"get_sysinfo":{}}}'
KASA_DAEMON_JSON_COUNTDOWN_DELETE_AND_RUN   = b'{"count_down":{"delete_all_rules":null,"add_rule":{"enable":1,"delay":300,"act":0,"name":"fail safe"}}}'
KASA_DAEMON_JSON_PLUG_ON                    = b'{"system":{"set_relay_state":{"state":1}},"count_down":{"delete_all_rules":null,"add_rule":{"enable":1,"delay":300,"act":0,"name":"fail safe"}}}'
KASA_DAEMON_JSON_PLUG_OFF                   = b'{"count_down":{"delete_all_rules":null},"system":{"set_relay_state":{"state":0}}}'
KASA_DAEMON_JSON_COUNTDOWN_DELETE           = b'{"count_down":{"delete_all_rules":null}}'
SSR_CONTROL_BOARD_REV_ss                    = "**"
SSR_CONTROL_BOARD_REV_sA                    = "*A"
SSR_CONTROL_BOARD_REV_sB                    = "*B"
SSR_CONTROL_BOARD_REV_sC                    = "*C"
SSR_CONTROL_BOARD_DISABLED                  = "None"
SSR_CONTROL_BOARD_DETECT_REV                = "Auto"
SSR_CONTROL_BOARD_PINS                      = {
    "LED":{
        "red":{
            SSR_CONTROL_BOARD_REV_ss:22,
            SSR_CONTROL_BOARD_REV_sA:23,
            SSR_CONTROL_BOARD_REV_sB:2,
            SSR_CONTROL_BOARD_REV_sC:2
        },
        "green":{
            SSR_CONTROL_BOARD_REV_ss:23,
            SSR_CONTROL_BOARD_REV_sA:22,
            SSR_CONTROL_BOARD_REV_sB:3,
            SSR_CONTROL_BOARD_REV_sC:3
        }
    },
    "Buzzer":{
        SSR_CONTROL_BOARD_REV_ss:13,
        SSR_CONTROL_BOARD_REV_sA:13,
        SSR_CONTROL_BOARD_REV_sB:12,
        SSR_CONTROL_BOARD_REV_sC:12
    },
    "Relay":{
        SSR_CONTROL_BOARD_REV_ss:12,
        SSR_CONTROL_BOARD_REV_sA:12,
        SSR_CONTROL_BOARD_REV_sB:13,
        SSR_CONTROL_BOARD_REV_sC:13
    },
    "Switch":{
        SSR_CONTROL_BOARD_REV_ss:-1,
        SSR_CONTROL_BOARD_REV_sA:-1,
        SSR_CONTROL_BOARD_REV_sB:-1,
        SSR_CONTROL_BOARD_REV_sC:6
    }
}
SSR_CONTROL_BOARD_VALUES_STANDARD           = 1
SSR_CONTROL_BOARD_VALUES_INVERTED           = 0
SSR_CONTROL_BOARD_VALUES_UNSUPPORTED        = -1
SSR_CONTROL_BOARD_REV_PINS                  = [14, 15, 18, 23, 24, 25, 8, 7, 16, 20, 21]
# TODO: Fix the board id numbers
SSR_CONTROL_BOARD_REV_MAP                   = {
    1793: SSR_CONTROL_BOARD_REV_sB,
    22: SSR_CONTROL_BOARD_REV_sC
}
SSR_CONTROL_BOARD_VALUES                    = {
    "LED":{
        "red":{
            SSR_CONTROL_BOARD_REV_ss:SSR_CONTROL_BOARD_VALUES_INVERTED,
            SSR_CONTROL_BOARD_REV_sA:SSR_CONTROL_BOARD_VALUES_INVERTED,
            SSR_CONTROL_BOARD_REV_sB:SSR_CONTROL_BOARD_VALUES_INVERTED,
            SSR_CONTROL_BOARD_REV_sC:SSR_CONTROL_BOARD_VALUES_STANDARD
        },
        "green":{
            SSR_CONTROL_BOARD_REV_ss:SSR_CONTROL_BOARD_VALUES_INVERTED,
            SSR_CONTROL_BOARD_REV_sA:SSR_CONTROL_BOARD_VALUES_INVERTED,
            SSR_CONTROL_BOARD_REV_sB:SSR_CONTROL_BOARD_VALUES_INVERTED,
            SSR_CONTROL_BOARD_REV_sC:SSR_CONTROL_BOARD_VALUES_STANDARD
        }
    },
    "Buzzer":{
        SSR_CONTROL_BOARD_REV_ss:SSR_CONTROL_BOARD_VALUES_INVERTED,
        SSR_CONTROL_BOARD_REV_sA:SSR_CONTROL_BOARD_VALUES_INVERTED,
        SSR_CONTROL_BOARD_REV_sB:SSR_CONTROL_BOARD_VALUES_INVERTED,
        SSR_CONTROL_BOARD_REV_sC:SSR_CONTROL_BOARD_VALUES_INVERTED
    },
    "Relay":{
        SSR_CONTROL_BOARD_REV_ss:SSR_CONTROL_BOARD_VALUES_INVERTED,
        SSR_CONTROL_BOARD_REV_sA:SSR_CONTROL_BOARD_VALUES_INVERTED,
        SSR_CONTROL_BOARD_REV_sB:SSR_CONTROL_BOARD_VALUES_INVERTED,
        SSR_CONTROL_BOARD_REV_sC:SSR_CONTROL_BOARD_VALUES_INVERTED
    },
    "Switch":{
        SSR_CONTROL_BOARD_REV_ss:SSR_CONTROL_BOARD_VALUES_UNSUPPORTED,
        SSR_CONTROL_BOARD_REV_sA:SSR_CONTROL_BOARD_VALUES_UNSUPPORTED,
        SSR_CONTROL_BOARD_REV_sB:SSR_CONTROL_BOARD_VALUES_UNSUPPORTED,
        SSR_CONTROL_BOARD_REV_sC:SSR_CONTROL_BOARD_VALUES_STANDARD
    }
}