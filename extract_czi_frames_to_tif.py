import os
import sys
import numpy as np
from aicsimageio import AICSImage
from aicsimageio.writers.ome_tiff_writer import OmeTiffWriter
from tqdm import tqdm


def save_czi_mosaics_as_tiff(czi_path, new_folder_path=None):
    """
    Written tiff files are problematic. Somehow Cellpose doesn't distinguish between channels. Why?
    """

    # Check if the given path is a .czi file
    if not czi_path.lower().endswith('.czi'):
        print("The provided file is not a .czi file.")

    # Read the .czi file
    img = AICSImage(czi_path, 
                    reconstruct_mosaic=False)
    
    # Get the scenes
    scenes = img.scenes
    
    # Extract directory path and filename from the provided path
    directory, filename = os.path.split(czi_path)

    # Initialize the OmeTiffWriter
    writer = OmeTiffWriter()

    # Loop over scenes
    for i, scene in tqdm(enumerate(img.scenes), desc="Looping over scenes"):
        # Set the scene
        img.set_scene(scene)
        print(f"Working on {scene}, contains {img.dims.M} mosaics (M)")

        # Create a new folder name based on the .czi filename (without extension)
        folder_name = os.path.splitext(filename)[0] + "scene_" + str(scene) + "_mosaics"
        
        # Construct the full path for the new folder
        new_folder_path = os.path.join(directory, folder_name)
        
        # Create the folder if it doesn't already exist
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            print(f"Folder created: {new_folder_path}")
        else:
            print(f"Folder already exists: {new_folder_path}")
        
        # Iterate over dimensions of the data and load into the memory
        for T in range(img.dims.T):
            for Z in range(img.dims.Z):
                for M in tqdm(range(img.dims.M), desc="Looping over mosaics"):
                    for C in range(img.dims.C):
                        frame_data_oom = img.get_image_dask_data("YX", T=T, Z=Z, M=M, C=C)
                        frame_data_im = frame_data_oom.compute()    # This will get the numpy array of the current frame in memory
            
                        # Construct the filename for the current frame
                        frame_filename = os.path.join(new_folder_path, f"{scene}_T{T}_Z{Z}_M{M}_{img.channel_names[C]}.ome.tiff")

                        # Save the numpy array as a .tif file
                        writer.save(
                            data = frame_data_im,
                            uri = frame_filename,
                            dim_order = "YX",
                            #physical_pixel_sizes = img.physical_pixel_sizes,
                            channel_names = img.channel_names[C],
                            #channel_colors = [[0, 255, 0], [255, 0, 0], [0, 0, 255]]
                        )

    print(f"Finished extracting mosaics.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/your/file.czi")
    else:
        czi_file_path = sys.argv[1]
        save_czi_mosaics_as_tiff(czi_file_path)
