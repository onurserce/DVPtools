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
from tifffile import imread, imwrite
from concurrent.futures import ThreadPoolExecutor


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

    n_channels = image.shape[-1]
    channels = {}
    for n in range(n_channels):
        channels[n] = image[:, :, n]

    return channels


def write_channels_into_seperate_folders(channels: dict, output_dir):
    print(channels[1])
    print(len(channels))
    print(output_dir)
    pass


def write_channels(channels: dict, output_dir, original_image_path: str, replace: [None, str] = None):
    # ToDo: make a folder called seperate_channels
    for channel in channels.keys():
        replaced_image_name = original_image_path.replace(replace, "_c{}_".format(channel))
        final_path = os.path.join(output_dir, replaced_image_name)
        imwrite(final_path, data=channels[channel])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", "-i", help="Path to the directory containing multichannel images")
    parser.add_argument("--image_format", "-f", default=".tiff", help="e.g. '.tiff' or '.png', defaults to tiff")
    parser.add_argument("--slurm_array_task_id", "-s", type=int, help="slurm array task id")
    parser.add_argument("--batch_size", "-b", type=int, help="number of files to process per task")
    parser.add_argument("--output_dir", "-o", default=None, help="Path to the output directory. Defaults to None, "
                                                                 "which creates a new directory for each channel "
                                                                 "inside the input_dir")
    args = parser.parse_args()

    selected_files = subset_files(directory=args.input_dir,
                                  file_extension=args.image_format,
                                  n_files=args.batch_size,
                                  slurm_array_task_id=args.slurm_array_task_id)

    # Todo: Read the image, Seperate into channels, write channels into seperate folders

    with ThreadPoolExecutor() as executor:
        futures = []
        for img in images:
            futures.append(executor.submit(cellpose_segment, [img], ...))
        for future in futures:
            results.append(future.result())

    # for file in selected_files:
    #     channels = seperate_image_into_channels(file)
    #     break
    #     write_channels_into_seperate_folders

# ToDo: This script is unfinished.
