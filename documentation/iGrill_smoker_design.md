# iGrill Smoker Design

Copyright &copy; 2019 Scott Atkins
<!-- markdownlint-disable MD033 -->
<h2>Table of Contents</h2>
<!-- markdownlint-enable MD033 -->
<!-- markdownlint-disable MD007 -->
<!-- markdownlint-disable MD010 -->
<!-- markdownlint-disable MD039 -->
<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Introduction](#introduction)
- [Sources](#sources)
- [Files](#files)
  - [Bash](#bash)
  - [Python](#python)
  - [INI](#ini)
  - [JSON](#json)
  - [CSV](#csv)
- [File relation graph](#file-relation-graph)
  - [/start_smoking.sh](#start_smokingsh)
  - [/scripts/config.sh](#scriptsconfigsh)
  - [/scripts/monitor.py](#scriptsmonitorpy)
  - [/scripts/data.sh](#scriptsdatash)
- [Configuration](#configuration)
  - [INI File](#ini-file)
- [How to Generate a Smoke Schedule](#how-to-generate-a-smoke-schedule)

<!-- /code_chunk_output -->
<!-- markdownlint-enable MD007 -->
<!-- markdownlint-enable MD010 -->
<!-- markdownlint-enable MD039 -->
## Introduction

There are a lot of moving parts in this project, so this is an attempt to document those parts and how they interact.  Additionally this a moving target, so some information can be out of date.

## Sources

Like most projects this has come from a number of different sources.

- [Github iGrill](https://github.com/kvantetore/igrill)
- [Bash ini Parser](https://github.com/rudimeier/bash_ini_parser)
- [Path helper](https://stackoverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself)
- [Highcharts](https://www.highcharts.com/)
- [tplink-smarthome-api](https://www.npmjs.com/package/tplink-smarthome-api)

## Files

This is an attempt to document all the files in the project.  Relations between files is shown [below](#file-relation-graph).

### Bash

- **[igrill-smoker/start_smoking.sh](../start_smoking.sh)** - The main script to start a smoking session.
  - Loads [paths.sh](../scripts/utils/paths.sh)
  - Loads [leds.sh](../scripts/utils/leds.sh)
  - Loads [kasa.sh](../scripts/utils/kasa.sh)
  - Loads [limits.sh](../scripts/utils/limits.sh)
  - Loads [config.sh](../scripts/config.sh)
  - Cleans up after the last run
  - Resets the limits
  - Resets the LEDs
  - Finds iGrill device if needed
  - Creates list of CSV files
  - Creates new CSV file and links it to current.csv
  - Stats [scripts/py_utils/kasa_daemon.py](../scripts/py_utils/kasa_daemon.py) to control the plug state
  - Resets the BT device on the Raspberry Pi
  - Calls [scripts/monitor.py](../scripts/monitor.py) to capture data over bluetooth
  - On Exit
    - Uses [scripts/py_utils/kasa_client.py](../scripts/py_utils/kasa_client.py) to stop [scripts/py_utils/kasa_daemon.py](../scripts/py_utils/kasa_daemon.py)
    - Cleans up run files
    - Resets the LEDs
- **[igrill-smoker/scripts/config.sh](../scripts/config.sh)** - Loads configuration
  - Loads [read_ini.sh](../scripts/utils/read_ini.sh)
  - Loads [defaults.sh](../scripts/utils/defaults.sh)
  - Loads [food script](../config/stage/)
- **[igrill-smoker/scripts/data.sh](../scripts/data.sh)** - Handles temperature data
  - Loads [paths.sh](../scripts/utils/paths.sh)
  - Loads [config.sh](../scripts/config.sh)
  - Determines if it is time to load the next stage
    - If so writes stage.sh and reloads [config.sh](../scripts/config.sh)
  - Reads last_temp.sh
  - Adjusts LEDs based on stage, temperature, and battery
  - Plays sounds based on stage, temperature, and battery
  - Sets the plug state based on history and current temperature
  - Writes state.json
  - Writes last_temp.sh
  - Writes data to current.csv
  - Calls to [scripts/pygrill/kasa/kasa_client.py](../scripts/pygrill/kasa/kasa_client.py) to get the plug state
  - Calls to [scripts/pygrill/board/ssrc_client.py](../scripts/pygrill/board/ssrc_client.py) to adjust the solid state relay
  - Calls to [scripts/pygrill/board/buzzer_client.py](../scripts/pygrill/board/buzzer_client.py) to sound alarms
  - Calls to [scripts/pygrill/board/leds.py](../scripts/pygrill/board/leds.py) to set the LEDs
- **[igrill-smoker/scripts/utils/bt.sh](../scripts/utils/bt.sh)** - Bluetooth functions
  - **BtReset** - Resets Bluetooth
- **[igrill-smoker/scripts/utils/create_vars.sh](../scripts/utils/create_vars.sh)** - Setup default values
  - Reads iGrill_config.example.ini
  - Creates default.sh
- **[igrill-smoker/scripts/utils/defaults.sh](../scripts/utils/defaults.sh)** - Config default values if iGrill_config.ini does not exist
- **[igrill-smoker/scripts/utils/gen_json.sh](../scripts/utils/gen_json.sh)** - Creates JSON file for Website
  - Loads [paths.sh](../scripts/utils/paths.sh)
  - Finds all CSV files that match the date format
  - Writes a JSON file with the list of files
- **[igrill-smoker/scripts/utils/get_mac.sh](../scripts/utils/get_mac.sh)** - Creates mac_config.py based on iGrill Bluetooth address
  - Loads [bt.sh](../scripts/utils/bt.sh)
  - Calls BtReset
  - Starts a scan for iGrill
    - Scan is killed when iGrill is found
  - Writes mac_config.py
  - Calls BtReset
- **[igrill-smoker/scripts/utils/limits.sh](../scripts/utils/limits.sh)** - Sets upper and lower limits for the iGrill
  - Loads [paths.sh](../scripts/utils/paths.sh)
  - Reset limits - Sets limits for all 4 probes to be -32768 to 32767
  - SetLimits - Sets limits for a particular probe
  - PrintLimits - Output set limits in an INI format
  - WriteLimits - Uses PrintLimits to write to a file
- **[igrill-smoker/scripts/utils/paths.sh](../scripts/utils/paths.sh)** - Sets up standard path variables
- **[igrill-smoker/scripts/utils/read_ini.sh](../scripts/utils/read_ini.sh)** - Reads ini file
  - read_ini - Reads the specified file and sets variables
- **igrill-smoker/run/stage.sh** - Tracks the current cooking stage
- **igrill-smoker/run/last_temp.sh** - Tracks the last temperature
- **[igrill-smoker/tests/board/board_checkout.sh](../tests/board/board_checkout.sh)** - Runs through a set of tests to check the board is functioning properly
  - LEDs
  - Buzzer

### Python

- **[igrill-smoker/scripts/pygrill/bt_monitor.py](../scripts/pygrill/bt_monitor.py)** - Top level python script
  - Loads the configuration
  - Formats the results
  - Calls [scripts/data.sh](../scripts/data.sh) with the temperature data
- **[igrill-smoker/scripts/pygrill/bluetooth/igrill.py](../scripts/pygrill/bluetooth/igrill.py)** - Interface to iGrill
  - Performs handshake
  - Grabs temperature/battery data
  - Sets probe limits
- **[igrill-smoker/scripts/pygrill/common/local_logging.py](../scripts/pygrill/common/local_logging.py)** - Sets up logging
  - Report specific log level
  - Redirects to file if specified
- **[igrill-smoker/scripts/pygrill/common/constant.py](../scripts/pygrill/common/constant.py)** - Various constants
- **[igrill-smoker/scripts/pygrill/board/board.py](../scripts/pygrill/board/board.py)** - Detects the board type
  - Cannot detect **, *A or *D.1
- **[igrill-smoker/scripts/pygrill/board/buzzer_daemon.py](../scripts/pygrill/board/buzzer_daemon.py)** - Controls the buzzer
  - plays different sounds for smoking complete and low battery
- **[igrill-smoker/scripts/pygrill/board/buzzer_client.py](../scripts/pygrill/board/buzzer_client.py)** - Passes commands to the daemon
  - done or low_battery for those tones
  - Tells the daemon to exit
- **[igrill-smoker/scripts/pygrill/kasa/kasa_daemon.py](../scripts/pygrill/kasa/kasa_daemon.py)** - Controls kasa hardware
  - Find plug by name
  - Return plug status
  - Sets countdown timer for 10 minutes when turning the plug on
- **[igrill-smoker/scripts/pygrill/kasa/kasa_client.py](../scripts/pygrill/kasa/kasa_client.py)** - Passes commands to the daemon
  - Turn plug on and off
  - Return plug status
  - Tells the daemon to exit
- **[igrill-smoker/scripts/pygrill/board/ssrc_daemon.py](../scripts/pygrill/board/ssrc_daemon.py)** - Controls solid state relay
  - Minimum is 30% max is 85%
  - Step up by 5% or 0.25%
  - Step down by 1% or 20%
  - Sets countdown timer for 10 minutes
  - On exit, kill Kasa daemon
- **[igrill-smoker/scripts/pygrill/board/ssrc_client.py](../scripts/pygrill/board/ssrc_client.py)** - Passes commands to the daemon
  - Turn up or down, a large or small amount
  - Leave everything the same, but reset the countdown
  - Tells the daemon to exit
- **[igrill-smoker/scripts/pygrill/board/leds.py](../scripts/pygrill/board/leds.py)** - Controls LEDs
  - Sets smoking complete or low battery
  - Sets temperature state:
    - Cold: low outside of band
    - Cool: low in band
    - Perfect: at target temperature
    - Warm: high in band
    - Hot: high out of band
- **igrill-smoker/scripts/pygrill/config/mac_config.py** - Mac address for the iGrill

### INI

- **[iGrill_config.ini](../config/iGrill_config.example.ini)** - Main configuration
- **limits.ini** - iGrill upper and lower limits for alarm

### JSON

- **state.json** - Current state of the smoking for website processing
- **items.json** - A list of csv files which can put into highcharts

### CSV

- **current.csv** - The current data set

## File relation graph

This is broken down into multiple graphs so it is easier to follow.

- Dotted lines are file reads/writes
- Bold lines are system calls to execute a script
- Normal lines are standard includes

### /start_smoking.sh

![start_smoking](assets/start_smoking.svg)

### /scripts/config.sh

![config](assets/config.svg)

### /scripts/monitor.py

![monitor](assets/monitor.svg)

### /scripts/data.sh

![data](assets/data.svg)

## Configuration

### INI File

The ini file is a one place for the user to configure this project.

<!-- NOTE: Add > at the end of this line and open markdown preview enhanced window.  Use shift enter to regenerate. --
```bash {cmd hide modify_source}
echo -n \`\`\`ini
cat ../config/iGrill_config.example.ini
```
<!-- -->
<!-- code_chunk_output -->

```ini
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
[iGrill]
# can be Standard or Mini
Type=Standard

[Probes]
# For iGrill mini set food probe to 0 and smoke probe to 1

# Food probe must be set between 0 and 4, where 0 means the
# probe is disabled.  The left most probe is 1 and right most
# is 4 on the iGrill 2/3
#
# If you disable the food probe, you must use a stage that
# is iGrill mini compatible (see stage file) or disable stages
FoodProbe=1

# Smoke probe must be set between 1 and 4.  The left most probe
# is 1 and right most is 4 on the iGrill 2/3
SmokeProbe=4

[Logging]
LogLevel=INFO
LogFile=

[Kasa]
# Name of your plug in the Kasa app, case sensitive
Name=iGrill-smoker

[Smoking]
MaxTempChange=2
TempBandSize=7

# Can be the name of any file in the stages directory (excluding the .sh) or None
Food=brisket

# Only valid if Food=None
SmokeMid=225
InternalTarget=185

# Used to specify the solid state relay board
[SSR]
# Possible values:
#  **, *A, *B, *C, *D, *D.1, *E, Auto, None
Board=Auto

[Reporting]
# time in seconds between polls of the iGrill
# faster polling means more power use
PollTime=20

ResultsDirectory=/var/www/html
CSVFile=current.csv
StateFile=state.json

```
<!-- /code_chunk_output -->

## How to Generate a Smoke Schedule

Easiest way is to copy then edit an existing schedule.  Examples and variable description is below.

Here is what **[igrill-smoker/config/stages/brisket.py](../config/stages/brisket.py)** looks like:
<!-- NOTE: Add > at the end of this line and open markdown preview enhanced window.  Use shift enter to regenerate. --
```bash {cmd hide modify_source}
echo \`\`\`bash
cat ../config/stages/brisket.sh
echo ""
echo -n \`\`\`
```
<!-- -->
<!-- code_chunk_output -->

```bash
#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# Defining variables for other scripts
# shellcheck disable=2034
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

MINI_COMPATIBLE=false

# Note: for this to work. Internal temp must be increased at each stage
# the system will go to the next stage when the food hits the designated
# internal temp

case "$STAGE" in
    1)
        # Warmup stage, keep plate at a cooler temp and limit temp rise
        STAGE_NAME="Warmup"
        SMOKE_MID=180
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=70
    ;;
    2)
        # Smoke stage, keep plate at cooler temp, but allow bigger temp rise
        STAGE_NAME="Smoke"
        SMOKE_MID=180
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=120
    ;;
    3)
        # Cook stage, move hotplate to higher temp, allow bigger temp rise
        STAGE_NAME="Cook"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=170
    ;;
    4)
        # Braise stage, move hotplate to higher temp, allow bigger temp rise
        STAGE_NAME="Braise"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=185
    ;;
    5|6)
        # Keep warm stage, move hotplate to higher temp, allow bigger temp rise
        STAGE_NAME="Keep warm"
        SMOKE_MID=160
        MAX_TEMP_CHANGE=2
        INTERNAL_TEMP=190
        # signal we're done
        FD_DONE=1
        # Stay in this stage
        STAGE=5
    ;;
    *)
        echo "error: unknown stage"
        exit 1
    ;;
esac
```

<!-- /code_chunk_output -->

- ```$STAGE``` - Current stage as an integer
  - Must start at 1
  - Case statement for the last stage (5 in the example) must also include last stage + 1 (eg. ```5|6```)
  - Last stage must set ```$STAGE``` to the last stage again in case it was incremented (eg. ```STAGE=5```)
- ```$STAGE_NAME``` - Name to show on the webpage for this stage
- ```$INTERNAL_TEMP``` - Target food temperature for this stage
  - Should be monotonically increasing for every stage except the last one
  - Use of ```$INTERNAL_TEMP``` means ```$MINI_COMPATIBLE``` should be false
- ```$SMOKE_MID``` - Temperature the smoke should be kept at
- ```$FD_DONE```- The value ```1``` indicates the food is done (set on the last stage)
- ```$MAX_TEMP_CHANGE``` - Maximum change over a time period.  Should be 2-4

Here is what **[igrill-smoker/config/stages/baby-back-ribs.py](../config/stages/baby-back-ribs.py)** looks like:

<!-- NOTE: Add > at the end of this line and open markdown preview enhanced window.  Use shift enter to regenerate. --
```bash {cmd hide modify_source}
echo \`\`\`bash
cat ../config/stages/baby-back-ribs.sh
echo ""
echo -n \`\`\`
```

<!-- code_chunk_output -->

```bash
#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# Defining variables for other scripts
# shellcheck disable=2034
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}

MINI_COMPATIBLE=true

case "$STAGE" in
    1)
        # Warmup stage, keep plate at a cooler temp
        STAGE_NAME="Warmup"
        SMOKE_MID=180
        MAX_TEMP_CHANGE=2
        TIME=15
    ;;
    2)
        # Smoke stage, keep plate at cooler temp
        STAGE_NAME="Smoke"
        SMOKE_MID=180
        MAX_TEMP_CHANGE=2
        TIME=180
    ;;
    3)
        # Cook stage, move hotplate to higher temp
        STAGE_NAME="Cook"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        TIME=120
    ;;
    4)
        # Sauce stage
        STAGE_NAME="Sauce"
        SMOKE_MID=225
        MAX_TEMP_CHANGE=2
        TIME=60
    ;;
    5|6)
        # Keep warm stage, move hotplate to lower temp
        STAGE_NAME="Keep warm"
        SMOKE_MID=165
        MAX_TEMP_CHANGE=2
        TIME=100
        # signal we're done
        FD_DONE=1
        # Stay in this stage
        STAGE=5
    ;;
    *)
        echo "error: unknown stage"
        exit 1
    ;;
esac
```

<!-- /code_chunk_output -->

This is iGrill mini compatible and uses the time instead of food temperature

- ```$TIME``` - Minutes to stay in this stage

Both ```$TIME``` and ```$INTERNAL_TEMP``` can be used in a stage, first event to occur moves the system to the next stage.
