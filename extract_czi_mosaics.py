import os
import logging
from aicsimageio import AICSImage
from tifffile import imwrite
from tqdm import tqdm
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='extract_czi_mosaics.py.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def extract_czi_mosaics_as_tiffs(path_to_czi_file: str,
                                 output_folder_path: Optional[str] = None,
                                 separate_channels: bool = True) -> None:
    """
    Extracts individual mosaics from a CZI file and saves them as TIFF images.

    Each mosaic from the CZI file is saved as a separate TIFF image. If separate_channels
    is set to True, each channel is saved as a separate file.

    Parameters:
    - path_to_czi_file (str): The path to the .czi file.
    - output_folder_path (str, optional): The path to the output folder. If not specified,
                                          the TIFFs are saved in a folder adjacent to the CZI file.
    - separate_channels (bool, default=True): Whether to save each channel as a separate TIFF.

    Returns:
    - None
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
                    # Save each channel separately
                    for C in range(img.dims.C):
                        mosaic_data_oom = img.get_image_dask_data(dimension_order_out="YXC", T=T, Z=Z, M=M, C=C)
                        mosaic_data_im = mosaic_data_oom.compute()  # Get the np array of the mosaic in memory

                        # Construct the filename for the current frame
                        mosaic_name = f"{scene}_T{T}_Z{Z}_M{M}_{img.channel_names[C]}.tiff"
                        mosaic_filename = os.path.join(output_folder_path, mosaic_name)

                        # Save the numpy array as a .tiff file
                        imwrite(mosaic_filename, mosaic_data_im)

    print(f"Finished extracting mosaics.")


def main(args):
    extract_czi_mosaics_as_tiffs(
        path_to_czi_file=args.czi_file_path,
        output_folder_path=args.output_folder_path,
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="Extract CZI mosaics as TIFF images.",
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('czi_file_path',
                        help="Path to the .czi file.")
    parser.add_argument('--output-folder-path',
                        help="Path to the output folder.", default=None)

    args = parser.parse_args()
    main(args)
