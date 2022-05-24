#!/bin/bash -e
rm -fr kafkaenv __pycache__
# create new venv
python3 -m venv kafkaenv
# activate venv
. kafkaenv/bin/activate
# install requirements
# a fresh venv comes with an old version of pip
# for some of these requirements to work we must upgrade pip in the venv
python3 -m pip install --upgrade pip
pip install -r requirements.txt