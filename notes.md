# David's recommendations for mask operations

- https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html
- https://github.com/hoerlteam/YeastMate/blob/main/examples/tracking.ipynb
- https://github.com/stardist/stardist/blob/main/stardist/matching.py#L109

# ThermoRawFileParser speed tests (n=1 each :()

- **srun -c 16**
  - 2024-05-10 17:09:37 INFO Started parsing data/test_data/20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_50_shape_0.raw
  - 2024-05-10 17:17:30 INFO Finished parsing data/test_data/20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_50_shape_0.raw
  - 7 minutes 53 seconds
- **srun -c 2**
  - 2024-05-10 17:20:14 INFO Started parsing data/test_data/20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_50_shape_0.raw
  - 2024-05-10 17:28:31 INFO Finished parsing data/test_data/20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_50_shape_0.raw
  - 8 minutes 17 seconds
- **srun -c 1**
  - 2024-05-10 17:40:42 INFO Started parsing data/test_data/20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_50_shape_0.raw
  - 2024-05-10 17:54:44 INFO Finished parsing data/test_data/20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_50_shape_0.raw
  - 14 minutes 02 seconds

#### The metadata is just awesome! Use it for setting up the DIA-NN search...

# Can mono-6.12.0.199 directory be removed?
- Probably.. go to raven02 and attach to tmux. If the job completed, the answer is yes!

# Other required software
- QuickNII
  - Check out https://www.nitrc.org/frs/?group_id=1341
  - For Mac: [QuickNII-ABAMouse-v3-2017.dmg](https://www.nitrc.org/frs/download.php/11553/QuickNII-ABAMouse-v3-2017.dmg)

