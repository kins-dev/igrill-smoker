#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# shellcheck disable=2034
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}
iGrill__ALL_SECTIONS='iGrill Probes Logging Kasa Smoking Reporting'
iGrill__ALL_VARS='iGrill__iGrill__Type iGrill__Probes__FoodProbe iGrill__Probes__SmokeProbe iGrill__Logging__LogLevel iGrill__Logging__LogFile iGrill__Kasa__Name iGrill__Smoking__MaxTempChange iGrill__Smoking__TempBandSize iGrill__Smoking__Food iGrill__Smoking__SmokeMid iGrill__Smoking__InternalTarget iGrill__Reporting__PollTime iGrill__Reporting__ResultsDirectory iGrill__Reporting__CSVFile iGrill__Reporting__StateFile'
iGrill__Kasa__Name=iGrill-smoker
iGrill__Logging__LogFile=
iGrill__Logging__LogLevel=INFO
iGrill__NUMSECTIONS=6
iGrill__Probes__FoodProbe=1
iGrill__Probes__SmokeProbe=4
iGrill__Reporting__CSVFile=current.csv
iGrill__Reporting__PollTime=20
iGrill__Reporting__ResultsDirectory=/var/www/html
iGrill__Reporting__StateFile=state.json
iGrill__Smoking__Food=brisket
iGrill__Smoking__InternalTarget=185
iGrill__Smoking__MaxTempChange=2
iGrill__Smoking__SmokeMid=225
iGrill__Smoking__TempBandSize=7
iGrill__iGrill__Type=Standard
