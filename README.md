# DVPtools
Codebase for everything related to the DVP pipeline.

*Switching to MannLabs tools as of 25.04.2024*
- [alphabase](https://github.com/MannLabs/alphabase)
- [py-lmd](https://github.com/MannLabs/py-lmd)
- [SPARCSpy](https://github.com/MannLabs/SPARCSpy)

## Installation

### Installation via Anaconda/miniconda

This is the recommended way of installation for most users.

1) Install Anaconda or miniconda
2) Clone the repository `git clone --recurse-submodules https://github.com/onurserce/DVPtools.git` and navigate inside `cd path/to/your/DVPtools`
3) Create a new environment with the recipe file DVPtools.yaml `conda env create -f DVPtools.yaml` (**INFO:** use _DVPtools_headless.yaml_ for headless systems)
4) Activate the environment `conda activate DVPtools`
5) Install alphabase, SPARCSpy and py-lmd editable using pip `pip install -e alphabase/. py-lmd/. SPARCSpy/.`
6) [Optional] Run `conda list > conda_list.txt` and `pip freeze > pip_freeze.txt` to keep a record of all installed packages with their versions
7) Install DIA-NN 1.8.1 (https://github.com/vdemichev/DiaNN/releases/tag/1.8.1)

### Installation into UNIX based systems (e.g. HPCs)

This is a partially automated way to install the project into UNIX based systems. If you don't understand what that
means, stick with the instructions above. Otherwise, assuming that you have conda installed and cloned the repo with its
submodules (steps 1 and 2 above):

1) Execute the bash installation script in the repository (e.g. `bash install_headless.sh`) and you should be done!
2) Similarly, execute DIA-NN installation script (e.g. `bash install_diann_headless.sh`)

## Usage via GUI

1) Initiate the DVP GUI (located under DeepVisualProteomics/gui) `python path/to/gui.py`
2) Create a new project by choosing a location and giving it a name (or load an existing project from a project config.yaml file)
