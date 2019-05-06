#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}
git clone https://git.kins.dev/igrill-smoker
cd igrill-smoker/install
bash run-install.sh
