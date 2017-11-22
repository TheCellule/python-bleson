#!/usr/bin/env bash

# Build dist
rm -fr dist build
python3 setup.py sdist
twine upload --repository pypitest dist/*

# Test dist
rm -fr env/test
virtualenv --no-site-packages env/test
cd env/test/bin
source activate
pip3 install --upgrade pip setuptools wheel

pip3 install  --no-cache-dir  --index-url https://test.pypi.org/simple/  bleson
python3 -m bleson --observer
deactivate
cd -



