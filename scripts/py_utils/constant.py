# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
KASA_NET_BUFFER_SIZE = 2048
KASA_NET_HEADER_SIZE = 4
KASA_NET_DISCOVER_IP = "255.255.255.255"
KASA_NET_PORT = 9999
KASA_JSON_DISCOVER = b'{"system":{"get_sysinfo":{}}}'
KASA_JSON_COUNTDOWN_DELETE_AND_RUN = b'{"count_down":{"delete_all_rules":null,"add_rule":{"enable":1,"delay":300,"act":0,"name":"fail safe"}}}'
KASA_JSON_PLUG_ON = b'{"system":{"set_relay_state":{"state":1}},"count_down":{"delete_all_rules":null,"add_rule":{"enable":1,"delay":300,"act":0,"name":"fail safe"}}}'
KASA_JSON_PLUG_OFF = b'{"count_down":{"delete_all_rules":null},"system":{"set_relay_state":{"state":0}}}'
KASA_JSON_COUNTDOWN_DELETE = b'{"count_down":{"delete_all_rules":null}}'
