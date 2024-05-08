# DVPtools
Codebase for everything related to the DVP pipeline.

*Switching to MannLabs tools as of 25.04.2024*
- [alphabase](https://github.com/MannLabs/alphabase)
- [py-lmd](https://github.com/MannLabs/py-lmd)
- [SPARCSpy](https://github.com/MannLabs/SPARCSpy)

## Installation via Anaconda/miniconda
1) Clone the repository `git clone --recurse-submodules https://github.com/onurserce/DVPtools.git` and navigate inside `cd path/to/your/DVPtools`
2) Create a new environment with the recipe file DVPtools.yaml `conda env create -f DVPtools.yaml`. For headless systems like computing clusters, use DVPtools_headless.yaml instead.
3) Activate the environment `conda activate DVPtools`
4) Install alphabase, SPARCSpy and py-lmd editable using pip `pip install -e alphabase/. py-lmd/. SPARCSpy/.`
5) [Optional] Run `conda list > conda_list` and `pip freeze > pip_freeze.txt` to keep a record of all installed packages with their versions

## Usage via GUI
1) Initiate the DVP GUI (located under DeepVisualProteomics/gui) `python path/to/gui.py`
2) Create a new project by choosing a location and giving it a name (or load an existing project from a project config.yaml file)
