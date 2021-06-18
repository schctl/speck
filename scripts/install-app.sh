#!/usr/bin/env sh

cd $(dirname $(realpath $0))/../
python -m pip install .
python -m pip install -r app/requirements.txt
