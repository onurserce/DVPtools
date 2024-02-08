#!/home/edwin/anaconda3/envs/cellpose/bin/python

import os
import pandas as pd
import sys
from cellpose import core, utils, io, models, metrics
import time
from tqdm import tqdm


# ToDo: Externalize the output folder
# ToDo: Externalize channels

def timefn(prior_time):
    seconds = time.time()-prior_time
    m,s=divmod(seconds,60)
    h,m=divmod(m,60)
    print(f'## THIS TOOK {h:.0f} hours {m:.0f} minutes {s:.0f} seconds')

def make_a_status_csv(path_to_dir, file_extension = ".tiff"):

    # Check if already exists
    if os.path.exists(os.path.join(path_to_dir, "Status.csv")):
        print("Status.csv already exists.")
        return
    else:
        df = pd.DataFrame(
            index = [os.path.join(path_to_dir, x) for x in os.listdir(path_to_dir) if x.endswith(file_extension)],
            columns = ['cellpose_masks']
        )

        df.sort_index().to_csv(os.path.join(path_to_dir, "Status.csv"))
        print("Status.csv created.")

def update_status_csv(path_to_status_csv):

    status = pd.read_csv(path_to_status_csv, index_col=0)
    
    im_dir_path = os.path.split(path_to_status_csv)[0]
    mask_dir_path = os.path.join(im_dir_path, "cellpose_masks")

    for path in status.index:
        hypothetical_mask_path = os.path.join(mask_dir_path, os.path.split(path[:-5])[-1] + "_cp_masks.tif")
        
        if os.path.exists(hypothetical_mask_path):
            status.loc[path, "cellpose_masks"] = True
        else:
            status.loc[path, "cellpose_masks"] = False

    status.to_csv(path_to_status_csv)


def cellpose_segment(im_dir, batch_size, gpu=False, channels=[3,1]):
    
    # Create masks folder if it doesn't already exists
    mask_dir = os.path.join(im_dir, 'cellpose_masks')
    try:
        os.mkdir(mask_dir)
    except FileExistsError as err:
        print("Directory", mask_dir, "already exists, continuing...")

    # Load Status.csv to continue from where the segmentation was interrupted
    if os.path.exists(os.path.join(im_dir, "Status.csv")):
        print("Status.csv found.")
        status = pd.read_csv(os.path.join(im_dir, "Status.csv"), index_col=0)
        im_paths = status.loc[status.loc[:, "cellpose_masks"] == False].index.to_list()
    else:
        print("Status.csv not found, creating a new one.")
        make_a_status_csv(im_dir)
        update_status_csv(os.path.join(im_dir, "Status.csv"))
        status = pd.read_csv(os.path.join(im_dir, "Status.csv"), index_col=0)
        im_paths = status.loc[status.loc[:, "cellpose_masks"] == False].index.to_list()

    print(f"## RUNNING CELLPOSE WITH 'batch_size = {batch_size}'")
    model = models.CellposeModel(gpu=gpu, model_type='cyto2')

    for i in tqdm(range(0, len(im_paths), batch_size)):
        
        images = [io.imread(f) for f in im_paths[i:i+batch_size]]

        masks, flows, styles = model.eval(images, 
                                        channels=channels,
                                        diameter=100,
                                        flow_threshold=0,
                                        cellprob_threshold=-2,
                                        min_size=40)

        mask_paths = [
            os.path.join(mask_dir, os.path.split(x)[-1]) for x in im_paths if
             '_c0_' in x if x.endswith('tiff')][i:i+batch_size]

        io.save_masks(images,
                    masks,
                    flows,
                    mask_paths,
                    channels=['gray'],
                    png=False,
                    tif=True,
                    save_txt=False,
                    save_flows=False,
                    save_outlines=False)
        
        update_status_csv(os.path.join(im_dir, "Status.csv"))

    """     mask_paths_original = [os.path.join(mask_dir, x) for x in os.listdir(mask_dir)]
        for x in mask_paths_original:
            os.rename(x, x.replace('_cp_masks', '')) """ # Why?


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py path/to/your/RGBs batch_size")
    else:
        start_timer = time.time()
        im_dir = sys.argv[1]
        try:
            batch_size = int(sys.argv[2])
        except Exception as err:
            print(err)
            batch_size = 1
            "Setting the batch size to 1 and continuing..."

        cellpose_segment(im_dir=im_dir, batch_size=batch_size)
        timefn(start_timer)
        print("Finished successfully.")