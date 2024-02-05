import os
import sys
import numpy as np
from aicsimageio import AICSImage
import tifffile
from tqdm import tqdm


def save_czi_frames_as_tiff(czi_path, new_folder_path=None):
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

    # Loop over scenes
    for i, scene in tqdm(enumerate(img.scenes), desc="Looping over scenes"):
        # Set the scene
        img.set_scene(scenes[i])
        print(f"Working on {scenes[i]}")

        # Create a new folder name based on the .czi filename (without extension)
        folder_name = os.path.splitext(filename)[0] + "scene_" + str(scene) + "_frames"
        
        # Construct the full path for the new folder
        new_folder_path = os.path.join(directory, folder_name)
        
        # Create the folder if it doesn't already exist
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            print(f"Folder created: {new_folder_path}")
        else:
            print(f"Folder already exists: {new_folder_path}")
        
        # Get the total number of frames in that scene
        frames = img.dims.M
        print(f"Total frames (M) in the file: {frames}")
        
        # Iterate over each frame and save as a .tif file
        for i2 in tqdm(range(frames)):
            frame_data_oom = img.get_image_dask_data("ZCYX", T=0, M=i2)
            frame_data_im = frame_data_oom.compute()    # This will get the numpy array of the current frame in memory
            
            # Construct the filename for the current frame
            frame_filename = os.path.join(new_folder_path, f"{scenes[i]}_frame_{i2}.tif")
            
            # Save the numpy array as a .tif file
            tifffile.imwrite(frame_filename, frame_data_im)
        
    print(f"Finished extracting frames.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/your/file.czi")
    else:
        czi_file_path = sys.argv[1]
        save_czi_frames_as_tiff(czi_file_path)
