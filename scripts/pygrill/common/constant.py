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


class KASA_DAEMON:
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


class BUZZ_DAEMON:
    PYRO_HOST = KASA_DAEMON.PYRO_HOST
    PYRO_PORT = KASA_DAEMON.PYRO_PORT + 1
    PYRO_OBJECT_ID = "PyGrillBuzzer"


class SSRC_DAEMON:
    PYRO_HOST = BUZZ_DAEMON.PYRO_HOST
    PYRO_PORT = BUZZ_DAEMON.PYRO_PORT + 1
    PYRO_OBJECT_ID = "PyGrillSSR"


class SSR_CONTROL:
    BOARD_REV_ss = "**"
    BOARD_REV_sA = "*A"
    BOARD_REV_sB = "*B"
    BOARD_REV_sC = "*C"
    BOARD_REV_sD = "*D"
    BOARD_DISABLED = "None"
    BOARD_DETECT_REV = "Auto"

    BOARD_VALUES_STANDARD = 1
    BOARD_VALUES_INVERTED = 0
    BOARD_VALUES_UNSUPPORTED = -1

    BOARD_REV_PINS = [14, 15, 18, 23, 24, 25, 8, 7, 16, 20, 21]

    BOARD_REV_MAP = {
        1793: BOARD_REV_sB,
        1794: BOARD_REV_sC,
        1795: BOARD_REV_sD
    }

    BOARD_ITEM_IO = "Pin"
    BOARD_ITEM_VALUE = "Value"
    BOARD_ITEM_INVALID = {
        BOARD_ITEM_IO: BOARD_VALUES_UNSUPPORTED,
        BOARD_ITEM_VALUE: BOARD_VALUES_UNSUPPORTED
    }
    BOARD_ITEMS = {
        "LED": {
            "Low battery": {
                BOARD_REV_ss: {
                    BOARD_ITEM_IO: 22,
                    BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
                },
                BOARD_REV_sA: {
                    BOARD_ITEM_IO: 23,
                    BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
                },
                BOARD_REV_sB: {
                    BOARD_ITEM_IO: 2,
                    BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
                },
                BOARD_REV_sC: {
                    BOARD_ITEM_IO: 2,
                    BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
                },
                BOARD_REV_sD: {
                    BOARD_ITEM_IO: 10,
                    BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
                }
            },
            "Smoking complete": {
                BOARD_REV_ss: {
                    BOARD_ITEM_IO: 23,
                    BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
                },
                BOARD_REV_sA: {
                    BOARD_ITEM_IO: 22,
                    BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
                },
                BOARD_REV_sB: {
                    BOARD_ITEM_IO: 3,
                    BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
                },
                BOARD_REV_sC: {
                    BOARD_ITEM_IO: 3,
                    BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
                },
                BOARD_REV_sD: {
                    BOARD_ITEM_IO: 22,
                    BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
                }
            },
            "Cold": {
                BOARD_REV_ss: BOARD_ITEM_INVALID,
                BOARD_REV_sA: BOARD_ITEM_INVALID,
                BOARD_REV_sB: BOARD_ITEM_INVALID,
                BOARD_REV_sC: BOARD_ITEM_INVALID,
                BOARD_REV_sD: {
                    BOARD_ITEM_IO: 2,
                    BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
                }
            },
            "Cool": {
                BOARD_REV_ss: BOARD_ITEM_INVALID,
                BOARD_REV_sA: BOARD_ITEM_INVALID,
                BOARD_REV_sB: BOARD_ITEM_INVALID,
                BOARD_REV_sC: BOARD_ITEM_INVALID,
                BOARD_REV_sD: {
                    BOARD_ITEM_IO: 3,
                    BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
                }
            },
            "Perfect": {
                BOARD_REV_ss: BOARD_ITEM_INVALID,
                BOARD_REV_sA: BOARD_ITEM_INVALID,
                BOARD_REV_sB: BOARD_ITEM_INVALID,
                BOARD_REV_sC: BOARD_ITEM_INVALID,
                BOARD_REV_sD: {
                    BOARD_ITEM_IO: 4,
                    BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
                }
            },
            "Warm": {
                BOARD_REV_ss: BOARD_ITEM_INVALID,
                BOARD_REV_sA: BOARD_ITEM_INVALID,
                BOARD_REV_sB: BOARD_ITEM_INVALID,
                BOARD_REV_sC: BOARD_ITEM_INVALID,
                BOARD_REV_sD: {
                    BOARD_ITEM_IO: 17,
                    BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
                }
            },
            "Hot": {
                BOARD_REV_ss: BOARD_ITEM_INVALID,
                BOARD_REV_sA: BOARD_ITEM_INVALID,
                BOARD_REV_sB: BOARD_ITEM_INVALID,
                BOARD_REV_sC: BOARD_ITEM_INVALID,
                BOARD_REV_sD: {
                    BOARD_ITEM_IO: 27,
                    BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
                }
            },
        },
        "Buzzer": {
            BOARD_REV_ss: {
                BOARD_ITEM_IO: 13,
                BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
            },
            BOARD_REV_sA: {
                BOARD_ITEM_IO: 13,
                BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
            },
            BOARD_REV_sB: {
                BOARD_ITEM_IO: 12,
                BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
            },
            BOARD_REV_sC: {
                BOARD_ITEM_IO: 12,
                BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
            },
            BOARD_REV_sD: {
                BOARD_ITEM_IO: 12,
                BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
            }
        },
        "Relay": {
            BOARD_REV_ss: {
                BOARD_ITEM_IO: 12,
                BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
            },
            BOARD_REV_sA: {
                BOARD_ITEM_IO: 12,
                BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
            },
            BOARD_REV_sB: {
                BOARD_ITEM_IO: 13,
                BOARD_ITEM_VALUE: BOARD_VALUES_INVERTED
            },
            BOARD_REV_sC: {
                BOARD_ITEM_IO: 13,
                BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
            },
            BOARD_REV_sD: {
                BOARD_ITEM_IO: 13,
                BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
            }
        },
        "Switch": {
            BOARD_REV_ss: BOARD_ITEM_INVALID,
            BOARD_REV_sA: BOARD_ITEM_INVALID,
            BOARD_REV_sB: BOARD_ITEM_INVALID,
            BOARD_REV_sC: {
                BOARD_ITEM_IO: 6,
                BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
            },
            BOARD_REV_sD: {
                BOARD_ITEM_IO: 6,
                BOARD_ITEM_VALUE: BOARD_VALUES_STANDARD
            }
        }
    }
