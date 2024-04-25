#!/bin/bash
#SBATCH -J run_cellpose
#SBATCH -o %J_%a.stdout
#SBATCH -e %J_%a.stderr
#SBATCH -a 0-15
#SBATCH -t 20:00
#SBATCH -c 8
#SBATCH --mem=16G
#SBATCH --mail-type=END
#SBATCH --mail-user=onur_serce@psych.mpg.de

# batch_size=10 used around peak 2Gb memory (per array task) and took around 5mins with -c=2

module purge
source "$HOME"/.bashrc
source activate DVP

this_script=${0}
channel=${1?Error: no channel given}
run_cellpose=${2?Error: no run_cellpose_yaml file given}
images_dir=${3?Error: no images_dir given}

# Prepare data folders
main_output_dir="$images_dir"/output
channel_output_dir="$main_output_dir"/channel_$channel
mkdir -p "$channel_output_dir"
# Continue with copying the data to /ptmp

# $SLURM_ARRAY_TASK_ID will be used as an index to a python script
srun python DeepVisualProteomics/hpc/run_cellpose.py "$channel" "$run_cellpose" "$images_dir" "$channel_output_dir" "$SLURM_ARRAY_TASK_ID"

# Save the scripts for reproducibility purposes
cp "$this_script" "$main_output_dir"
cp DeepVisualProteomics/hpc/run_cellpose.py "$main_output_dir"
# Continue with copying of the data back to the home folder
# Remove files in /ptmp/

# If preparation (zipping and copying of files back and forth can be made in a seperate script, that'd awesome.)

# I need to log the commit hash... git rev-parse HEAD together with the git diff and config file
# install pre-commit, it runs certain things before committing
# Check pre-commit.com