#!/bin/bash
pip install virtualenv # install virtualenv if not already

python -m venv ./.env # create virtual environment
source ./.env/bin/activate # activate virtual environment

pip install -r docs/requirements.txt # install requirements