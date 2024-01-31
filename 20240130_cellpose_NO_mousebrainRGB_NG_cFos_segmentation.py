#!/home/edwin/anaconda3/envs/cellpose/bin/python


import numpy as np
import matplotlib.pyplot as plt
from cellpose import core, utils, io, models, metrics
import os
import time
import tkinter as tk
import re
#import datetime
from tifffile import imread, imwrite
from tqdm.notebook import tqdm
import time


def timefn(prior_time):
    seconds = time.time()-prior_time
    m,s=divmod(seconds,60)
    h,m=divmod(m,60)
    print(f'## THIS STEP TOOK {h:.0f} hours {m:.0f} minutes {s:.0f} seconds')

# start_dir = '/media/axioscan/01_Users/EdRo/20230723_mouseBrain_10um_NucGreen_EDFstitch_tiffs/'
# im_dir = '/media/axioscan/01_Users/EdRo/20230723_mouseBrain_10um_NucGreen_EDFstitch_tiffs/'
im_dir = '/media/data4tb/dvp_dat/Onur/20240125_Onur_15um_NG_555cfos_647neun_RGBs/'


# scene_list = []
# for (root, dirs, files) in os.walk(start_dir):
#     for dirname in dirs:
#         if dirname.startswith('scene'):
#             scene_list.append(os.path.join(root, dirname))


# for im_dir in scene_list:
# #for im_dir in [scene_list[0]]:
#     print(im_dir)
im_paths = [os.path.join(im_dir,x) for x in os.listdir(im_dir) if '_c0_' in x]

print('## READING IMAGES FOR {} FILES'.format(len(im_paths)))
start_timer = time.time()
images = [io.imread(f) for f in im_paths]
timefn(start_timer)

print('## RUNNING CELLPOSE')
start_timer = time.time()
model = models.CellposeModel(gpu=True, model_type='cyto2')
masks, flows, styles = model.eval(images, 
                                  channels=[2,1],
                                diameter=100,
                                flow_threshold=0,
                                cellprob_threshold=-2,
                                min_size=40)

timefn(start_timer)

print('## PROCESSING AND SAVING CELLPOSE OUTPUT')
start_timer = time.time()
mask_dir = os.path.join(im_dir, 'cellpose_masks_NG_cFos')
# mask_dir = os.path.join('/media/data4tb/dvp_dat/', '20230723_mouseBrain_10um_NucGreen_cellpose_masks')
os.mkdir(mask_dir)

mask_paths = [os.path.join(mask_dir, x) for x in os.listdir(im_dir) if '_c0_' in x if x.endswith('tiff')]

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

mask_paths_original = [os.path.join(mask_dir, x) for x in os.listdir(mask_dir)]

for x in mask_paths_original:
    os.rename(x, x.replace('_cp_masks', ''))
timefn(start_timer)