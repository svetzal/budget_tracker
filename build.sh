#!/bin/bash

source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python setup.py py2app
