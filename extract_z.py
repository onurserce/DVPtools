# Adapted from the script of Rami Al-Maskari

import os
import tifffile
import numpy as np
import dask
import dask.array as da
import zarr
from dask.diagnostics import ProgressBar
from dask.distributed import Client
from tqdm import tqdm
import torch
from cellpose import models


client = Client()
ProgressBar().register()

zarr_fused_image_path = '/home/onurserce/Data/Helmholz/241025_20241025_OS_SN43_555cFos_647NeuN_horizontal_09-48-56/fused/fused_Zsquished.zarr'
zr = zarr.open(zarr_fused_image_path,
               mode='r')  # Persistence mode: ‘r’ means read only (must exist); ‘r+’ means read/write (must exist)
zr.tree()

img = da.from_zarr(zr.fused_tp_0_ch_1.s0)
img = img.compute()


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(torch.cuda.is_available())

model_gpu = models.CellposeModel(model_type='nuclei', device=device)

folder = '/home/onurserce/Data/Helmholz/241025_20241025_OS_SN43_555cFos_647NeuN_horizontal_09-48-56/SN_43_ch_1_zslices/SN43_masks'
for i in tqdm(range(img.shape[0])):
    masks, flows, styles = model_gpu.eval(x=[img[i, :, :]],
                                          channels=[0, 0],
                                          diameter=8,
                                          flow_threshold=3,
                                          cellprob_threshold=-5,
                                          batch_size=256,
                                          )
    mask = masks[0]
    tifffile.imwrite(file=os.path.join(folder, f"SN43_squished_ch1_Z_{i:04d}.tif"), data=mask)
print('done')

def save_tiff(img, path):
    if not (os.path.exists(path)):
        os.mkdir(path)
    output = []
    for z in range(img.shape[0]):
        print(z, end="\r", flush=True)
        final_path = os.path.join(path, f"SN43_squished_ch1_{z:04d}.tif")
        task = dask.delayed(tifffile.imwrite)(final_path, np.rot90(t.get_image_dask_data('YX', T=0, C=1, Z=z), k=1))
        output.append(task)
    dask.compute(*output)
    print('done!')


path_out = '/home/onurserce/Data/Helmholz/241025_20241025_OS_SN43_555cFos_647NeuN_horizontal_09-48-56/SN_43_ch_1_zslices'
save_tiff(t, path_out)
