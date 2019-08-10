#!/usr/bin/env python3
"""
  Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
                        (https://git.kins.dev/igrill-smoker)
  License:              MIT License
                        See the LICENSE file
"""

__author__ = "Scott Atkins"
__version__ = "1.4.0"
__license__ = "MIT"

import os

class CONFIG:
    if not 'IGRILL_BAS_DIR' in os.environ:
        BASEPATH = os.path.realpath(os.path.dirname(os.path.realpath(__file__))+"/../../../")
    else:
        BASEPATH = os.path.realpath(os.environ['IGRILL_BAS_DIR'])

class BLUETOOTH:
    TEMPERATURE_SCRIPT_NAME = "data.sh"

class TEST:
    class KASA:
        class DAEMON:
            DISCOVER_RSP = b'{"system":{"get_sysinfo":{"sw_ver":"0 Build 0 Rel.0","hw_ver":"0.0","type":"IOT.SMARTPLUGSWITCH","model":"00000(XX)","mac":"00:00:00:00:00:00","dev_name":"Wi-Fi Plug","alias":"iGrill-smoker","relay_state":0,"on_time":0,"active_mode":"none","feature":"TIM","updating":0,"icon_hash":"","rssi":-55,"led_off":0,"longitude_i":0,"latitude_i":0,"hwId":"0","fwId":"00000000000000000000000000000000","deviceId":"0","oemId":"0","err_code":0}}}'
            ON_NO_ERROR_RSP = b'{"system":{"set_relay_state":{"err_code":0}},"count_down":{"delete_all_rules":{"err_code":0},"add_rule":{"id":"D7F3ED1F8E813522BD9F673AD735E4C3","err_code":0}}}'
            OFF_NO_ERROR_RSP = b'{"count_down":{"delete_all_rules":{"err_code":0}},"system":{"set_relay_state":{"err_code":0}}}'
            OFF_ERROR_RSP = b'{"count_down":{"delete_all_rules":{"err_code":0}},"system":{"set_relay_state":{"err_code":1}}}'


class KASA:
    class DAEMON:
        NET_BUFFER_SIZE = 2048
        NET_HEADER_SIZE = 4
        NET_DISCOVER_IP = "255.255.255.255"
        NET_PORT = 9999

        PYRO_HOST = "localhost"
        PYRO_PORT = NET_PORT + 1
        PYRO_OBJECT_ID = "PyGrillKasa"
        JSON_DISCOVER = b'{"system":{"get_sysinfo":{}}}'
        JSON_COUNTDOWN_DELETE_AND_RUN = b'{"count_down":{"delete_all_rules":null,"add_rule":{"enable":1,"delay":300,"act":0,"name":"fail safe"}}}'
        JSON_PLUG_ON = b'{"system":{"set_relay_state":{"state":1}},"count_down":{"delete_all_rules":null,"add_rule":{"enable":1,"delay":300,"act":0,"name":"fail safe"}}}'
        JSON_PLUG_OFF = b'{"count_down":{"delete_all_rules":null},"system":{"set_relay_state":{"state":0}}}'
        JSON_COUNTDOWN_DELETE = b'{"count_down":{"delete_all_rules":null}}'


class BUZZ:
    class DAEMON:
        PYRO_HOST = KASA.DAEMON.PYRO_HOST
        PYRO_PORT = KASA.DAEMON.PYRO_PORT + 1
        PYRO_OBJECT_ID = "PyGrillBuzzer"

    class PWM:
        MAX = 1000000
        MIN = 0
        FREQ1 = 2000
        FREQ2 = 2500
        FREQ3 = 3000


class SSRC:
    class PWM:
        MAX = BUZZ.PWM.MAX
        MIN = BUZZ.PWM.MIN
        PERIOD = 101

    class TemperatureState:
        HOT = -1 * (BUZZ.PWM.MAX // 5)  # 20%
        WARM = -1 * (BUZZ.PWM.MAX // 100)  # 1%
        PERFECT = 0  # 0%
        COOL = 1 * (BUZZ.PWM.MAX // 100)  # -1%
        COLD = 1 * (BUZZ.PWM.MAX // 5)   # -20%

    class BOARD:
        REV_ss = "**"
        REV_sA = "*A"
        REV_sB = "*B"
        REV_sC = "*C"
        REV_sD = "*D"
        REV_sD_Patched = "*D.1"
        DISABLED = "None"
        DETECT_REV = "Auto"

        VALUES_STANDARD = 1
        VALUES_INVERTED = 0
        VALUES_UNSUPPORTED = -1

        REV_PINS = [14, 15, 18, 23, 24, 25, 8, 7, 16, 20, 21]

        REV_MAP = {
            1793: REV_sB,
            1794: REV_sC,
            1795: REV_sD
        }

        ITEM_IO = "Pin"
        ITEM_VALUE = "Value"
        ITEM_INVALID = {
            ITEM_IO: VALUES_UNSUPPORTED,
            ITEM_VALUE: VALUES_UNSUPPORTED
        }
        ITEMS = {
            "LED": {
                "Low battery": {
                    REV_ss: {
                        ITEM_IO: 22,
                        ITEM_VALUE: VALUES_INVERTED
                    },
                    REV_sA: {
                        ITEM_IO: 23,
                        ITEM_VALUE: VALUES_INVERTED
                    },
                    REV_sB: {
                        ITEM_IO: 2,
                        ITEM_VALUE: VALUES_INVERTED
                    },
                    REV_sC: {
                        ITEM_IO: 2,
                        ITEM_VALUE: VALUES_STANDARD
                    },
                    REV_sD: {
                        ITEM_IO: 10,
                        ITEM_VALUE: VALUES_STANDARD
                    },
                    REV_sD_Patched: {
                        ITEM_IO: 10,
                        ITEM_VALUE: VALUES_INVERTED
                    }
                },
                "Smoking complete": {
                    REV_ss: {
                        ITEM_IO: 23,
                        ITEM_VALUE: VALUES_INVERTED
                    },
                    REV_sA: {
                        ITEM_IO: 22,
                        ITEM_VALUE: VALUES_INVERTED
                    },
                    REV_sB: {
                        ITEM_IO: 3,
                        ITEM_VALUE: VALUES_INVERTED
                    },
                    REV_sC: {
                        ITEM_IO: 3,
                        ITEM_VALUE: VALUES_STANDARD
                    },
                    REV_sD: {
                        ITEM_IO: 22,
                        ITEM_VALUE: VALUES_STANDARD
                    },
                    REV_sD_Patched: {
                        ITEM_IO: 22,
                        ITEM_VALUE: VALUES_INVERTED
                    }
                },
                "Cold": {
                    REV_ss: ITEM_INVALID,
                    REV_sA: ITEM_INVALID,
                    REV_sB: ITEM_INVALID,
                    REV_sC: ITEM_INVALID,
                    REV_sD: {
                        ITEM_IO: 2,
                        ITEM_VALUE: VALUES_STANDARD
                    },
                    REV_sD_Patched: {
                        ITEM_IO: 2,
                        ITEM_VALUE: VALUES_INVERTED
                    }
                },
                "Cool": {
                    REV_ss: ITEM_INVALID,
                    REV_sA: ITEM_INVALID,
                    REV_sB: ITEM_INVALID,
                    REV_sC: ITEM_INVALID,
                    REV_sD: {
                        ITEM_IO: 3,
                        ITEM_VALUE: VALUES_STANDARD
                    },
                    REV_sD_Patched: {
                        ITEM_IO: 3,
                        ITEM_VALUE: VALUES_INVERTED
                    }
                },
                "Perfect": {
                    REV_ss: ITEM_INVALID,
                    REV_sA: ITEM_INVALID,
                    REV_sB: ITEM_INVALID,
                    REV_sC: ITEM_INVALID,
                    REV_sD: {
                        ITEM_IO: 4,
                        ITEM_VALUE: VALUES_STANDARD
                    },
                    REV_sD_Patched: {
                        ITEM_IO: 4,
                        ITEM_VALUE: VALUES_INVERTED
                    }
                },
                "Warm": {
                    REV_ss: ITEM_INVALID,
                    REV_sA: ITEM_INVALID,
                    REV_sB: ITEM_INVALID,
                    REV_sC: ITEM_INVALID,
                    REV_sD: {
                        ITEM_IO: 17,
                        ITEM_VALUE: VALUES_STANDARD
                    },
                    REV_sD_Patched: {
                        ITEM_IO: 17,
                        ITEM_VALUE: VALUES_INVERTED
                    }
                },
                "Hot": {
                    REV_ss: ITEM_INVALID,
                    REV_sA: ITEM_INVALID,
                    REV_sB: ITEM_INVALID,
                    REV_sC: ITEM_INVALID,
                    REV_sD: {
                        ITEM_IO: 27,
                        ITEM_VALUE: VALUES_STANDARD
                    },
                    REV_sD_Patched: {
                        ITEM_IO: 27,
                        ITEM_VALUE: VALUES_INVERTED
                    }
                },
            },
            "Buzzer": {
                REV_ss: {
                    ITEM_IO: 13,
                    ITEM_VALUE: VALUES_INVERTED
                },
                REV_sA: {
                    ITEM_IO: 13,
                    ITEM_VALUE: VALUES_INVERTED
                },
                REV_sB: {
                    ITEM_IO: 12,
                    ITEM_VALUE: VALUES_INVERTED
                },
                REV_sC: {
                    ITEM_IO: 12,
                    ITEM_VALUE: VALUES_STANDARD
                },
                REV_sD: {
                    ITEM_IO: 12,
                    ITEM_VALUE: VALUES_STANDARD
                },
                REV_sD_Patched: {
                    ITEM_IO: 12,
                    ITEM_VALUE: VALUES_STANDARD
                }
            },
            "Relay": {
                REV_ss: {
                    ITEM_IO: 12,
                    ITEM_VALUE: VALUES_INVERTED
                },
                REV_sA: {
                    ITEM_IO: 12,
                    ITEM_VALUE: VALUES_INVERTED
                },
                REV_sB: {
                    ITEM_IO: 13,
                    ITEM_VALUE: VALUES_INVERTED
                },
                REV_sC: {
                    ITEM_IO: 13,
                    ITEM_VALUE: VALUES_INVERTED
                },
                REV_sD: {
                    ITEM_IO: 13,
                    ITEM_VALUE: VALUES_STANDARD
                },
                REV_sD_Patched: {
                    ITEM_IO: 13,
                    ITEM_VALUE: VALUES_INVERTED
                }
            },
            "Switch": {
                REV_ss: ITEM_INVALID,
                REV_sA: ITEM_INVALID,
                REV_sB: ITEM_INVALID,
                REV_sC: {
                    ITEM_IO: 6,
                    ITEM_VALUE: VALUES_STANDARD
                },
                REV_sD: {
                    ITEM_IO: 6,
                    ITEM_VALUE: VALUES_STANDARD
                },
                REV_sD_Patched: ITEM_INVALID
            }
        }

    class DAEMON:
        PYRO_HOST = BUZZ.DAEMON.PYRO_HOST
        PYRO_PORT = BUZZ.DAEMON.PYRO_PORT + 1
        PYRO_OBJECT_ID = "PyGrillSSR"
