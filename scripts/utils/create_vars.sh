#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

source "read_ini.sh"
read_ini "../../config/iGrill_config.example.ini" --prefix iGrill
cat > "defaults.sh" <<EOL
#!/bin/bash
# shellcheck disable=2034
true
# shellcheck disable=2086
set -\$-ue\${DEBUG+xv}
EOL
set | grep "^iGrill" >> defaults.sh