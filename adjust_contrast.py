import os
import sys
import numpy as np
from aicsimageio import AICSImage
from aicsimageio.readers.ome_tiff_reader import OmeTiffReader
from aicsimageio.writers.ome_tiff_writer import OmeTiffWriter
from tqdm import tqdm
from skimage import exposure

folder = "/Users/onur_serce/MPIB/20240125_MPIB_15um/20240125_Onur_15um_NG_555cfos_647neun-_EDFvar-_stitchNoFuseEdgeDetectscene_ScanRegion0_mosaics"

files = [file for file in os.listdir(folder) if file.endswith("ome.tiff")]

# Initialize the OmeTiffWriter
writer = OmeTiffWriter()

for file in tqdm(files):
    reader = OmeTiffReader(os.path.join(folder, file))
    img = reader.get_image_data()[0,0,0]
    p2, p98 = np.percentile(img, (2, 98))
    img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))

    # Save the numpy array as a .tif file
    writer.save(
        data = img_rescale,
        uri = os.path.join(folder, file[:-9]+"ea.ome.tiff"),
        dim_order = "YX"
        #physical_pixel_sizes = img.physical_pixel_sizes,
        #channel_names = img.channel_names[C],
        #channel_colors = [[0, 255, 0], [255, 0, 0], [0, 0, 255]]
    )