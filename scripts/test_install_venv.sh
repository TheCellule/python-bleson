#!/usr/bin/env bash

# Install bleson into virtual env from PyPi (prod)

# Run in bash (Mac/Linux) or Git Shell (Windows)
_PY=python3
_PIP=pip3
_ENVNAME=prod
_BIN=env/$_ENVNAME/bin

if [ "$WINDIR" ]; then
    echo Windows
    _PY=python
    _BIN=env/$_ENVNAME/Scripts
fi

rm -fr env/$_ENVNAME
mkdir env 2> /dev/nul
virtualenv --no-site-packages env/$_ENVNAME
cd $_BIN
source activate
#$_PIP install --upgrade pip setuptools wheel
$_PIP install --no-cache-dir bleson
$_PY -m bleson --observer
deactivate
