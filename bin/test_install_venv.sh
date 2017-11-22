#!/usr/bin/env bash

# Install bleson into virtual env from PyPi (prod)

# Run in bash (Mac/Linux) or Git Shell (Windows)
_PY=python3
_PIP=pip3
_ENV_NAME=prod
_ENV_DIR=env/$_ENV_NAME
_ENV_BIN=$_ENV_DIR/bin
#_VENV_PY_ARG=--python=$_PY
_SUDO="sudo -E"

if [ "$WINDIR" ]; then
    echo Windows
    _PY=python
    _PIP=pip
    _ENV_BIN=$_ENV_DIR/Scripts
    _SUDO=
fi

rm -fr $_ENV_DIR
mkdir env 2> /dev/null

$_PY -m venv $_ENV_DIR --without-pip
source $_ENV_BIN/activate

$_PIP install --upgrade pip setuptools wheel
$_PIP install --no-cache-dir bleson
$_SUDO $_PY -m bleson --observer
deactivate

