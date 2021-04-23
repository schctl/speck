@echo off
cd %~dp0%/../
py -m pip install .
py -m pip install -r app/requirements.txt
