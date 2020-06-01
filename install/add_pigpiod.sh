#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
:
# shellcheck disable=2154
set -$-ue${DEBUG+xv}
LINE="@reboot /usr/bin/pigpiod"
(   
    crontab -l
    echo "${LINE}"
) | crontab -
