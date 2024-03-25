# DeepVisualProteomics
Codebase for anything related to DVP pipeline

## Installation 
1) Create a conda environment with the recipe DVP.yaml `conda env create -f DVP.yaml`
2) Clone cellpose fork `git clone https://github.com/onurserce/cellpose.git`
3) `conda activate DVP`
4) Change directory to where cellpose fork is cloned `cd cellpose`
5) Install the fork with `pip install -e .`

## Usage via GUI
1) Initiate the DVP GUI (located under DeepVisualProteomics/gui) `python path/to/gui.py`
2) Create a new project by choosing a location and giving it a name (or load an existing project from a project config.yaml file)