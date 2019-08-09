#!/bin/bash
# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
# Some cam processors have trouble with my rev scheme,
# so this removes that line from the gerber
# shellcheck disable=2034
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}


if ! [ "$#" -eq "1" ]; then
    echo "Wrong number of arguments to process_gerbers.sh"
    echo "Expected 1, got $#"
    exit 1
fi

if ! [ -d "$1" ]; then
    echo "Wrong argument type to process_gerbers.sh"
    echo "Expected a directory"
    exit 1
fi

if ! [ -d "${1}/Gerbers" ]; then
    echo "Wrong argument type to process_gerbers.sh"
    echo "Expected a directory with a Gerbers directory inside"
    exit 1
fi

if [ -e "${1}/Gerbers-2" ]; then
    echo "\"${1}/Gerbers-2\" exists, will not overwrite"
    exit 1
fi

mkdir "${1}/Gerbers-2"
if [ -f "${1}/Gerbers/gerbers.zip" ]; then
    rm -f "${1}/Gerbers/gerbers.zip"
fi

pushd "${1}/Gerbers"
for infile in *; do
    if [ -f "${infile}" ]; then
        outfile="Gerbers-2/${infile}"
        echo "\"${1}/Gerbers/${infile}\" -> \"${1}/${outfile}\""
        sed '/^G04 #@! TF.ProjectId,/d' "${infile}" > "../${outfile}"
    fi
done
popd
pushd "${1}/Gerbers-2"
zip "../Gerbers/gerbers.zip" ./*
popd

rm -rf "${1}/Gerbers-2"