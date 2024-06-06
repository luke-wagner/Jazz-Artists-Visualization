#!/usr/bin/env powershell
conda create -n jazz-artists-visualization pip  # create conda environment
conda activate jazz-artists-visualization       # activate conda environment

pip install -r docs/requirements.txt            # install python dependencies