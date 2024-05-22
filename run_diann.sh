#!/bin/bash
#SBATCH -J run_diann
#SBATCH -t 06:00:00
#SBATCH -c 16
#SBATCH --mem=32G
#SBATCH --mail-type=END
#SBATCH --mail-user=onur_serce@psych.mpg.de

temp_dir="$HOME"/temp
fasta_file="$HOME"/data/UP000000589_10090.fasta

diann-1.8.1 --f "$HOME"/data/test_data/20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_1000_shape_0.mzML --f "$HOME"/data/test_data/20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_50_shape_0.mzML --cut "K*,R*,!*P" --fasta "$fasta_file" --fasta-search --gen-spec-lib --max-pep-len 30 --max-pr-charge 6 --min-pep-len 6 --met-excision --min-pr-mz 300 --missed-cleavages 1 --out test_output --pg-level 1 --predictor --reanalyse --relaxed-prot-inf --report-lib-info --smart-profiling --temp "$temp_dir" --threads 32 --verbose 4 --var-mods 1
