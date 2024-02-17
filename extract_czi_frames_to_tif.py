#  ToDo: Add ArgumentParser (from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter).
#   Check out https://github.com/onurserce/campy/blob/9a7633f9eaae737606355ff67f0701aaea1d8f38/campy/campy.py for an
#   elegant usage of the ArgumentParser together with a config.yaml file.

#  ToDo: What's the best way to pass an argument to the script to tell if frames are to be extracted separately or not?

import os
import numpy as np
import sys
from aicsimageio import AICSImage
from tifffile import imwrite
from tqdm import tqdm


def save_czi_mosaics_as_tiffs(path_to_czi_file, separate_channels=True, output_folder_path=None):
    """
    Written tiff files are problematic. Somehow Cellpose doesn't distinguish between channels. Why?
    """

    # Check if the given path is a .czi file
    if not path_to_czi_file.endswith('.czi'):
        raise TypeError('The provided file is not a .czi file.')
    else:
        # Read the .czi file
        img = AICSImage(path_to_czi_file,
                        reconstruct_mosaic=False)  # This is important to not stitch the image

    # Get the scenes
    scenes = img.scenes
    print(f'Total number of scenes found: {len(scenes)}')

    # Extract directory path and filename from the provided path
    directory, filename = os.path.split(path_to_czi_file)
    filename_without_extension = os.path.splitext(filename)[0]

    if output_folder_path:
        output_folder_path = os.path.join(output_folder_path, filename_without_extension + '_czi_mosaics')
    else:
        output_folder_path = os.path.join(directory, filename_without_extension + '_czi_mosaics')

    # Create the output folder if it doesn't already exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        print(f"Folder created: {output_folder_path}")
    else:
        print(f"Folder already exists: {output_folder_path}")

    # Loop over scenes
    for i, scene in tqdm(enumerate(img.scenes), desc="Looping over scenes"):
        # Set the scene
        img.set_scene(scene)
        print(f"Working on {scene}, contains {img.dims.M} mosaics (M)")

        # Iterate over dimensions of the data and load into the memory
        for T in range(img.dims.T):
            for Z in range(img.dims.Z):
                for M in tqdm(range(img.dims.M), desc="Looping over mosaics"):
                    if separate_channels:
                        # Save each channel separately
                        for C in range(img.dims.C):
                            mosaic_data_oom = img.get_image_dask_data(dimension_order_out="YXC", T=T, Z=Z, M=M, C=C)
                            mosaic_data_im = mosaic_data_oom.compute()  # Get the np array of the mosaic in memory

                            # Construct the filename for the current frame
                            mosaic_name = f"{scene}_T{T}_Z{Z}_M{M}_{img.channel_names[C]}.tiff"
                            mosaic_filename = os.path.join(output_folder_path, mosaic_name)

                            # Save the numpy array as a .tiff file
                            imwrite(mosaic_filename, mosaic_data_im)
                    else:
                        # Save a multichannel image
                        channel_order = ['AF555', 'SYTOG', 'AF647']  # Order of channels will show up in CellPose as RGB

                        mosaic_data_oom = img.get_image_dask_data(dimension_order_out="YXC", T=T, Z=Z, M=M)
                        mosaic_data_im = mosaic_data_oom.compute()  # Get the np array of the mosaic in memory

                        empty_mosaic = [None] * len(channel_order)

                        for ch, channel in enumerate(channel_order):
                            empty_mosaic[ch] = mosaic_data_im[:, :, img.channel_names.index(channel)]

                        reordered_mosaic = np.dstack(empty_mosaic)

                        # Construct the filename for the current frame
                        channel_order_string = "-".join(channel_order)
                        mosaic_name = f"{scene}_T{T}_Z{Z}_M{M}_{channel_order_string}.tiff"
                        mosaic_filename = os.path.join(output_folder_path, mosaic_name)

                        # Save the numpy array as a .tiff file
                        imwrite(mosaic_filename, mosaic_data_im)

    print(f"Finished extracting mosaics.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/your/file.czi")
    else:
        czi_file_path = sys.argv[1]
        save_czi_mosaics_as_tiffs(czi_file_path)