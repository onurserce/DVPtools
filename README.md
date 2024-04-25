# DVPTools
Codebase for everything related to the DVP pipeline.

*Switching to MannLabs tools as of 25.04.2024*
- [alphabase](https://github.com/MannLabs/alphabase)
- [py-lmd](https://github.com/MannLabs/py-lmd)
- [SPARCSpy](https://github.com/MannLabs/SPARCSpy)

## Installation 
1) Clone the repository `git clone https://github.com/onurserce/DeepVisualProteomics.git`
2) Create a conda environment with the recipe DVP.yaml `conda env create -f DVP.yaml`
3) `conda activate DVP`
4) Optionally run `pip freeze > requirements.txt` to generate requirements file

## Usage via GUI
1) Initiate the DVP GUI (located under DeepVisualProteomics/gui) `python path/to/gui.py`
2) Create a new project by choosing a location and giving it a name (or load an existing project from a project config.yaml file)
