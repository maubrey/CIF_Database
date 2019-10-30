#! /bin/bash

BASEDIR=$(dirname "$0")
cd "$BASEDIR"
source $(python setup.py "PYTHON_PATH")
which python
python app.py
