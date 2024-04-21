#!/bin/bash
#SBATCH -J run_cellpose
#SBATCH -o %j_%A_%a.stdout
#SBATCH -e %j_%A_%a.stderr
#SBATCH -a 0-100
#SBATCH -t 10:00
#SBATCH --qos=short
#SBATCH -c 1
#SBATCH --mem=8G
#SBATCH --mail-type=END
#SBATCH --mail-user=onur_serce@psych.mpg.de

module purge
source "$HOME"/.bashrc
source activate DVP

channel=${1?Error: no channel given}
run_cellpose=${2?Error: no run_cellpose_yaml file given}
images_dir=${3?Error: no images_dir given}

output_dir="$images_dir"/output/channel_$channel
mkdir -p output_dir

# $SLURM_ARRAY_TASK_ID will be used as an index to a python script
python DeepVisualProteomics/hpc/run_cellpose.py "$channel" "$run_cellpose" "$images_dir" "$output_dir" "$SLURM_ARRAY_TASK_ID"