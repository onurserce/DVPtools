#!/bin/bash
#SBATCH -J run_ThermoRawFileParser.sh
#SBATCH -t 00:30:00
#SBATCH -c 16
#SBATCH --mem=32G
#SBATCH --mail-type=END
#SBATCH --mail-user=onur_serce@psych.mpg.de

mono ThermoRawFileParser/ThermoRawFileParser.exe -d="$HOME"/data/test_data -f=2 -m=1

