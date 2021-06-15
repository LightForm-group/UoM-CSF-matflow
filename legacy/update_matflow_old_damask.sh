#!/bin/bash

MATFLOW_SHEBANG=`head -n 1 ~/.local/bin/matflow`
MATFLOW_PYTHON=${MATFLOW_SHEBANG:2}

echo "Using Python: ${MATFLOW_PYTHON}"

module purge
module load apps/anaconda3/5.2.0/bin # should this match the shebang python in matflow script?
module load tools/env/proxy2

PACKAGES_ALL=(
    "matflow"\
    "damask-parse"\
    "formable"\
    "matflow-damask"\
    "matflow-formable"\
    "matflow-defdap"\
    "matflow-mtex"\
    "matflow-neper"\
    "matflow-demo-extension"\
)
PACKAGES_GREP=$(printf "\|%s" "${PACKAGES_ALL[@]}")
PACKAGES_GREP=${PACKAGES_GREP:2}

PACKAGES_VERSIONED=(
    "matflow"\
    "damask-parse==0.2.10"\
    "formable"\
    "matflow-damask==0.1.17"\
    "matflow-formable"\
    "matflow-defdap"\
    "matflow-mtex"\
    "matflow-neper"\
    "matflow-demo-extension"\
)

PACKAGES_UPDATE=$(printf " %s" "${PACKAGES_VERSIONED[@]}")
PACKAGES_UPDATE=${PACKAGES_UPDATE:1}

echo "Installed package versions are:"
$MATFLOW_PYTHON -m pip list --user | grep $PACKAGES_GREP

echo "Updating packages: ${PACKAGES_UPDATE}"
$MATFLOW_PYTHON -m pip install --user -U $PACKAGES_UPDATE

module unload apps/anaconda3/5.2.0/bin
