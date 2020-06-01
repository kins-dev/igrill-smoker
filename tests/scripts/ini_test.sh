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
INI__foo1__bar1=""
source "../../scripts/utils/read_ini.sh"
echo "Read complete"
read_ini "../data/test.ini"
set | grep "^INI"
echo "${INI__foo1__bar1}"
