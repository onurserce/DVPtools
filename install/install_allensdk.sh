conda create -n allensdk
conda activate allensdk
conda install python=3.10 h5py pip # Didn't work with more recent Python versions
pip install allensdk ipykernel  # Try installing ipykernel seperately if doesn't work
python -m ipykernel install --user --name=allensdk