#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

source "../../scripts/utils/read_ini.sh"
echo "Read complete"
read_ini "../data/test.ini"
set | grep "^INI"
echo "${INI__foo1__bar1}"