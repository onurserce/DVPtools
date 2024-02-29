#!/home/edwin/anaconda3/envs/cellpose/bin/python

import os
import sys
from cellpose import core, utils, io, models, metrics
import time
from tqdm import tqdm

def timefn(prior_time):
    seconds = time.time()-prior_time
    m,s=divmod(seconds,60)
    h,m=divmod(m,60)
    print(f'## THIS TOOK {h:.0f} hours {m:.0f} minutes {s:.0f} seconds')

def cellpose_segment(im_dir, batch_size):
 
    im_paths = [os.path.join(im_dir,x) for x in os.listdir(im_dir) if ('_c0_' in x and x.endswith(".tiff"))]
    mask_dir = os.path.join(im_dir, 'cellpose_masks')

    try:
        os.mkdir(mask_dir)
    except FileExistsError as err:
        print("Directory", mask_dir, "already exists, continuing...")

    print(f"## RUNNING CELLPOSE WITH 'batch_size = {batch_size}'")
    model = models.CellposeModel(gpu=False, model_type='cyto2')

    for i in tqdm(range(0, len(im_paths), batch_size)):
        
        images = [io.imread(f) for f in im_paths[i:i+batch_size]]

        masks, flows, styles = model.eval(images, 
                                        channels=[2,1],
                                        diameter=100,
                                        flow_threshold=0,
                                        cellprob_threshold=-2,
                                        min_size=40)

        mask_paths = [os.path.join(mask_dir, x) for x in os.listdir(im_dir) if '_c0_' in x if x.endswith('tiff')][i:i+batch_size]

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

    """     mask_paths_original = [os.path.join(mask_dir, x) for x in os.listdir(mask_dir)]
        for x in mask_paths_original:
            os.rename(x, x.replace('_cp_masks', '')) """ # Why



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