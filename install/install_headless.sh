#!/bin/bash
cd "$HOME"/DVPtools
source "$HOME"/.bashrc
conda env create -f DVPtools_headless.yaml
conda activate DVPtools
pip install -e alphabase/. py-lmd/. SPARCSpy/.
conda list > conda_list.txt
pip freeze > pip_freeze.txt
. "$HOME"/.bashrc
echo "install successful"