#! /bin/bash

BASEDIR=$(dirname "$0")
cd "$BASEDIR"
cd ../python
PY_Path=$(python setup.py "PYTHON_PATH")
source "$PY_Path"
which python
python ../python/app.py
