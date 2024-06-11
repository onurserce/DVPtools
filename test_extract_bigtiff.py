# Code modified by Omega at 2024-06-11 15:39:03.863581.
# Request:The code is producing error: ``` In [5]: extract_and_save_tiles(tiff_path, output_folder) --------------------------------------------------------------------------- AttributeError                            Traceback (most recent call last) Cell In[5], line 1 ----> 1 extract_and_save_tiles(tiff_path, output_folder)  Cell In[1], line 21, in extract_and_save_tiles(tiff_path, output_folder, tile_size, overlap_percent)      18 with tiff.TiffFile(tiff_path) as tif:      19     # Process each series in the TIFF file      20     for series_index, series in enumerate(tif.series): ---> 21         with series.asarray() as img:      22             # Calculate the step size based on the overlap      23             step_size = [int(dim * (1 - overlap_percent)) for dim in tile_size]      25             # Calculate the number of tiles in each dimension  AttributeError: __enter__  ```.

# Code modified by Omega at 2024-06-11 15:32:44.643279.
# Request: Fix the AttributeError when using series.asarray() in a context manager.

"""
Certainly! Below is the modified Python script that demonstrates how to extract tiles from all series in a TIFF file with a 10 percent overlap between tiles, and save them as individual TIFF files. This script uses the tifffile library to handle the TIFF operations. Make sure you have tifffile installed in your environment. If not, you can install it using pip install tifffile.

Python Script for Extracting Overlapping Tiles from All Series in a TIFF File
"""
    
import tifffile as tiff
import os

def extract_and_save_tiles(tiff_path, output_folder, tile_size=(512, 512), overlap_percent=0.1):
    """
    Extracts overlapping tiles from all series in a TIFF file and saves them as individual TIFF files.

    Parameters:
    - tiff_path: Path to the input TIFF file.
    - output_folder: Folder where the tiles will be saved.
    - tile_size: Size of the tiles (height, width).
    - overlap_percent: Percentage of overlap between tiles.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the TIFF file
    with tiff.TiffFile(tiff_path) as tif:
        # Process each series in the TIFF file
        for series_index, series in enumerate(tif.series):
            # Corrected the usage of series.asarray() without a context manager
            img = series.asarray()
            # Calculate the step size based on the overlap
            step_size = [int(dim * (1 - overlap_percent)) for dim in tile_size]

            # Calculate the number of tiles in each dimension
            n_tiles_x = (img.shape[1] - tile_size[1]) // step_size[1] + 1
            n_tiles_y = (img.shape[0] - tile_size[0]) // step_size[0] + 1

            # Loop over the image and extract tiles
            for i in range(n_tiles_y):
                for j in range(n_tiles_x):
                    # Define the tile's boundaries
                    y_start = i * step_size[0]
                    y_end = y_start + tile_size[0]
                    x_start = j * step_size[1]
                    x_end = x_start + tile_size[1]

                    # Extract the tile
                    tile = img[y_start:y_end, x_start:x_end]

                    # Save the tile as a TIFF file
                    tile_filename = f"series_{series_index}_tile_{i}_{j}.tif"
                    tile_path = os.path.join(output_folder, tile_filename)
                    tiff.imwrite(tile_path, tile)

                    print(f"Saved {tile_path}")

# Example usage
tiff_path = 'path_to_your_tiff_file.tif'
output_folder = 'path_to_output_tiles'
extract_and_save_tiles(tiff_path, output_folder)

"""
How to Use the Script
Replace 'path_to_your_tiff_file.tif' with the path to your TIFF file.
Replace 'path_to_output_tiles' with the path to the folder where you want to save the tiles.
This script will read the specified TIFF file, extract overlapping tiles from all series, and save each tile as a new TIFF file in the specified output folder. Adjust the tile_size and overlap_percent parameters as needed based on your specific requirements.
"""
