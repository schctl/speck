#!/bin/sh

# cd to root directory
cd $(dirname $(realpath $0))/../

python -m pip install .
python -m pip install -r app/requirements.txt
