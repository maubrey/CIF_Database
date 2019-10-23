#! /bin/bash

BASEDIR=$(dirname "$0")
cd "$BASEDIR"
cd ..
source $(python setup.py "PYTHON_PATH")
which python
python app.py

