#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# shellcheck source-path=SCRIPTDIR/scripts/utils
:
# shellcheck disable=2154
set -$-ue${DEBUG+xv}

# shellcheck source=read_ini.sh
source "read_ini.sh"
read_ini "../../config/iGrill_config.example.ini" --prefix iGrill
cat > "defaults.sh" << EOL
#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# shellcheck disable=2034
true
# shellcheck disable=2086
set -\$-ue\${DEBUG+xv}
EOL
set | grep "^iGrill" >> defaults.sh
