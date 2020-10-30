#! /bin/bash


BASEDIR=$(dirname "$0")
cd "$BASEDIR"
source $(python ../python/setup.py "PYTHON_PATH")
which python

pip install dash==1.4.1
pip install pandas