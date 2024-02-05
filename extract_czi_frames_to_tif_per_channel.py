
import os
import sys
import numpy as np
from aicsimageio import AICSImage
import tifffile
from tqdm import tqdm

def save_czi_frames_as_tiff(czi_path):
    # Check if the given path is a .czi file
    if not czi_path.lower().endswith('.czi'):
        print("The provided file is not a .czi file.")
        return

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
    img = AICSImage(czi_path, reconstruct_mosaic=False)
    
    # Get the total number of scenes (assuming scenes correspond to frames)
    scenes = img.dims.M
    print(f"Total scenes (M) in the file: {scenes}")
    
    # Iterate over each scene and save as a .tif file
    for i in tqdm(range(scenes)):
        frame_data_oom = img.get_image_dask_data("TZCYX", M=i)
        frame_data_im = frame_data_oom.compute()
        
        # Iterate over each channel in the frame
        for c in range(frame_data_im.shape[2]): # Assuming the channel dimension is the third
            channel_data = frame_data_im[:, :, c, :, :]
            
            # Construct the filename for the current frame and channel
            frame_channel_filename = os.path.join(new_folder_path, f"frame_{i}_c_{c}.tif")
            
            # Save the numpy array of the current channel as a .tif file
            tifffile.imwrite(frame_channel_filename, channel_data)
        
    print(f"Finished with extracting frames.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/your/file.czi")
    else:
        czi_file_path = sys.argv[1]
        save_czi_frames_as_tiff(czi_file_path)
