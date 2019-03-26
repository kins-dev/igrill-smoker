#!/bin/bash
set -ue
CSV_FILE=/var/www/html/current.csv
STATE_FILE=/var/www/html/state.json
BAD_DATA=65536
# Used to warn on low battery
MIN_BATTERY=15
TP_LINK_IP="192.168.0.1"

STAGE_NAME="Unknown"
# Set to 1 to use stages
STAGE=0
SMOKE_MID=225
INTERNAL_TEMP=190
MAX_TEMP_CHANGE=2

if [ -f "stage.sh" ]; then
	source stage.sh
fi

LAST_SM_TEMP=0
LAST_MT_TEMP=0
if [ -f "last_temps.sh" ]; then
	source last_temps.sh
fi

# Warmup stage, keep plate at a cooler temp and limit temp rise
if [ $STAGE -eq 1 ]; then
	STAGE_NAME="Warmup"
	SMOKE_MID=180
	MAX_TEMP_CHANGE=1
	INTERNAL_TEMP=70
fi
A
# Smoke stage, keep plate at cooler temp, but allow bigger temp rise
if [ $STAGE -eq 2 ]; then
	STAGE_NAME="Smoke"
	SMOKE_MID=180
	MAX_TEMP_CHANGE=2
	INTERNAL_TEMP=120
fi

# Cook stage, move hotplate to higher temp, allow bigger temp rise
if [ $STAGE -eq 3 ]; then
	STAGE_NAME="Cook"
	SMOKE_MID=225
	MAX_TEMP_CHANGE=2
	INTERNAL_TEMP=170
fi

# Braise stage, move hotplate to higher temp, allow bigger temp rise
if [ $STAGE -eq 4 ]; then
	STAGE_NAME="Braise"
	SMOKE_MID=225
	MAX_TEMP_CHANGE=2
	INTERNAL_TEMP=185
Afi

# Keep warm stage, move hotplate to higher temp, allow bigger temp rise
if [ $STAGE -ge 5 ]; then
	STAGE_NAME="Keep warm"
	SMOKE_MID=160
	MAX_TEMP_CHANGE=2
	INTERNAL_TEMP=190
	# Stay in this stage
	STAGE=5
fi
