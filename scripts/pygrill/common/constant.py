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


class SSRC:
    class BOARD:
        REV_ss = "**"
        REV_sA = "*A"
        REV_sB = "*B"
        REV_sC = "*C"
        REV_sD = "*D"
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
                    ITEM_VALUE: VALUES_INVERTED
                },
                REV_sD: {
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
                    ITEM_VALUE: VALUES_STANDARD
                },
                REV_sD: {
                    ITEM_IO: 13,
                    ITEM_VALUE: VALUES_STANDARD
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
                }
            }
        }

    class DAEMON:
        PYRO_HOST = BUZZ.DAEMON.PYRO_HOST
        PYRO_PORT = BUZZ.DAEMON.PYRO_PORT + 1
        PYRO_OBJECT_ID = "PyGrillSSR"
