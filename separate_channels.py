"""
Given a folder of multichannel images, extract each channel into a seperate folder.
Args:
    input_folder: folder containing multichannel images
    image_format: str. Defaults to ".tiff"
    output_dir: path. Defaults to None, which creates a new folder for each channel inside the input_folder
Returns:
"""
import os
import glob


def subset_files(directory, file_extension, n_files, slurm_array_task_id):
    """
    Subsets n_files files with the given extension to batch_size using the slurm_array_task_id
    Args:
        directory: path to directory containing files to subset.
        file_extension: extension of files to subset (e.g. ".tiff").
        n_files: number of files to subset.
        slurm_array_task_id: $SLURM_ARRAY_TASK_ID

    Returns: list containing paths for the subset of files with the given file_extension in directory
    """
    sorted_file_list = sorted(glob.glob(os.path.join(directory, "*" + file_extension)))  # sort for parallel execution
    selected_files = sorted_file_list[slurm_array_task_id * n_files:(slurm_array_task_id + 1) * n_files]
    return selected_files


def seperate_image_into_channels(image):
    """
    Assumes that the channel is the last dimension and min(image.shape) = number of channels
    Returns: dictionary containing each channel as key and its corresponding image as value.
    """

    if image.ndim != 3:
        raise ValueError("Input must be 3 dimensional")

    n_channels = min(image.shape)
    channels = {}
    for i in range(n_channels):
        single_channel = image[:, :, i]
        channels[i] = single_channel

    return channels


def write_channels_into_seperate_folders(channels, output_dir):
    print(channels[1])
    print(len(channels))
    print(output_dir)
    pass


if __name__ == "__main__":

    # import argparse
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument("input_folder", help="path to folder containing multichannel images")
    # parser.add_argument("image_format", default=".tiff", help="e.g. '.tiff' or '.png'")
    # parser.add_argument("output_dir", help="path to output folder")
    # args = parser.parse_args()

    import sys

    directory = sys.argv[1]
    n_files = int(sys.argv[2])   # This is $BATCH_SIZE
    slurm_array_task_id = int(sys.argv[3])
    file_extension = '.tiff'    # Static for now #ToDo: change later

    selected_files = subset_files(directory, file_extension, n_files, slurm_array_task_id)

    # for file in selected_files:
    #     channels = seperate_image_into_channels(file)
    #     break
    #     write_channels_into_seperate_folders

# ToDo: This script is unfinished.
