import os
import sys
import numpy as np
from aicsimageio import AICSImage
from tqdm import tqdm

czi_file_path = '/Users/onur_serce/MPIB/20240125_MPIB_15um/20240125_Onur_15um_NG_555cfos_647neun-_EDFvar-_stitchNoFuseEdgeDetect.czi'

# Read the .czi file
img = AICSImage(czi_file_path, 
                reconstruct_mosaic=False)

