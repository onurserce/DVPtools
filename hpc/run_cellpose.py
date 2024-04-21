"""
This script is meant to run cellpose segmentation on a folder of images on a HPC system and intended to be used together
with the run_cellpose.yaml configuration file and run_cellpose.sh Slurm batch job submission script.
"""

import os
import glob
import sys
from cellpose import io, models
import time
import yaml


def timefn(prior_time):
    seconds = time.time() - prior_time
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print(f'## THIS TOOK {h:.0f} hours {m:.0f} minutes {s:.0f} seconds')


def subset_tiffs(images_dir, batch_size, slurm_array_task_id):
    # Returns images and
    sorted_tiff_list = sorted(glob.glob(os.path.join(images_dir, '*.tiff')))  # sort for parallel execution
    selected_tiffs = sorted_tiff_list[slurm_array_task_id * batch_size:(slurm_array_task_id + 1) * batch_size]
    return selected_tiffs


def cellpose_segment(images, model, channels, diameter, flow_threshold, cellprob_threshold, min_size):
    model = models.CellposeModel(model_type=model)
    masks, flows, styles = model.eval(images,
                                      channels=channels,
                                      diameter=diameter,
                                      flow_threshold=flow_threshold,
                                      cellprob_threshold=cellprob_threshold,
                                      min_size=min_size)
    return masks, flows, styles


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python run_cellpose.py channels_to_segment run_cellpose.yaml images_dir output_dir "
              "slurm_array_task_id. \n Please note that output_dir must be created before running the segmentation.")
    else:
        start_timer = time.time()
        print(f"Segmentation started. Current time: {start_timer} ")

        # Script arguments
        channels_to_segment = [int(sys.argv[1]), 0]  # Todo: Modify this so that it supports multi-channel segmentation
        path_to_config_file = sys.argv[2]
        images_dir = sys.argv[3]
        output_dir = sys.argv[4]
        slurm_array_task_id = int(sys.argv[5])

        # Read remaining parameters from the run_cellpose.yaml file
        with open(path_to_config_file, 'r') as stream:
            config = yaml.safe_load(stream)

        # Subset and read in images
        selected_tiffs = subset_tiffs(images_dir, config['batch_size'], slurm_array_task_id)
        images = [io.imread(tiff) for tiff in selected_tiffs]

        # Generate masks
        masks, flows, styles = cellpose_segment(
            images=images,
            model=config['model'],
            channels=channels_to_segment,
            # Single channel for now, therefore not in the config file. To be changed later
            diameter=config['diameter'],
            flow_threshold=config['flow_threshold'],
            cellprob_threshold=config['cellprob_threshold'],
            min_size=config['min_size'])

        # Same as the original image names
        mask_names = [os.path.split(path)[-1] for path in selected_tiffs if path.endswith('.tiff')]

        # Save the output
        io.save_masks(images, masks, flows, mask_names, png=False, tif=True, channels=channels_to_segment,
                      suffix="", save_flows=True, save_outlines=True, dir_above=False, in_folders=True,
                      savedir=output_dir, save_txt=True, save_mpl=False)

        # ToDo: Copy the job submission script, configuration script and this script into the outputs folder. Can be
        #  made uneditable or even a single file
        print(f"This script is called with the following parameters: \n {sys.argv}")
        print(f"Config file: {config}")

        timefn(start_timer)
        print("Finished successfully.")
