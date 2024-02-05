import os
import sys
import numpy as np
from aicsimageio import AICSImage
import tifffile
from tqdm import tqdm


def save_czi_frames_as_tiff(czi_path, new_folder_path=None):
    """
    Extracts and saves individual frames from a CZI file as TIFF files.

    This function takes a file path to a CZI file as input, creates a directory for the frames extracted from this file,
    and saves each frame as a TIFF file within the newly created directory. It is designed to work with CZI files that
    contain multiple scenes or frames, where each scene is considered a separate frame. The function uses AICSImageIO
    for reading the CZI file and tifffile for writing the frames as TIFF files.
    """

    # Check if the given path is a .czi file
    if not czi_path.lower().endswith('.czi'):
        print("The provided file is not a .czi file.")
    
    # Extract directory path and filename from the provided path
    directory, filename = os.path.split(czi_path)
    
    # Create a new folder name based on the .czi filename (without extension)
    folder_name = os.path.splitext(filename)[0] + "_frames"
    
    # Construct the full path for the new folder
    new_folder_path = os.path.join(directory, folder_name)
    
    # Create the folder if it doesn't already exist
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder created: {new_folder_path}")
    else:
        print(f"Folder already exists: {new_folder_path}")
    
    # Read the .czi file
    img = AICSImage(czi_path,
                   reconstruct_mosaic=False)
    
    # Get the total number of scenes (assuming scenes correspond to frames)
    scenes = img.dims.M
    print(f"Total scenes (M) in the file: {scenes}")
    
    # Iterate over each scene and save as a .tif file
    for i in tqdm(range(scenes)):
        frame_data_oom = img.get_image_dask_data("TZCYX", M=i)
        frame_data_im = frame_data_oom.compute()
        frame_data_im = frame_data_im # This will get the numpy array of the current scene/frame
        
        # Construct the filename for the current frame
        frame_filename = os.path.join(new_folder_path, f"frame_{i}.tif")
        
        # Save the numpy array as a .tif file
        tifffile.imwrite(frame_filename, frame_data_im)
        
    print(f"Finished with extracting frames.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/your/file.czi")
    else:
        czi_file_path = sys.argv[1]
        save_czi_frames_as_tiff(czi_file_path)
