"diann.exe --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_25_shape_0.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_25_shape_1.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_25_shape_2.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_50_shape_0.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_50_shape_1.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_50_shape_2.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_125_shape_0.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_125_shape_1.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_125_shape_2.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_250_shape_0.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_250_shape_1.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_250_shape_2.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_500_shape_0.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_500_shape_1.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_500_shape_2.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_1000_shape_0.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_1000_shape_1.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_1000_shape_2.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_blank_0.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_blank_1.raw  --f C:\Users\onur.serce\Downloads\2024May_Onur\20240504_OA4_33min_EdRo_SA_ER586_Onur_Input_Experiment_slideB_blank_2.raw  --lib  --threads 32 --verbose 4 --out C:\Users\onur.serce\Downloads\2024May_Onur\diann output main\report.tsv --qvalue 0.01 --matrices --out-lib C:\Users\onur.serce\Downloads\2024May_Onur\diann output main\report-lib.tsv --gen-spec-lib --predictor --fasta C:\Users\onur.serce\ownCloud - Onur Serce (onse)@datashare.mpcdf.mpg.de\UP000000589_10090.fasta --fasta-search --min-fr-mz 200 --max-fr-mz 1800 --met-excision --cut K*,R* --missed-cleavages 1 --min-pep-len 6 --max-pep-len 32 --min-pr-mz 300 --max-pr-mz 1800 --min-pr-charge 1 --max-pr-charge 6 --unimod4 --var-mods 1 --double-search --individual-mass-acc --individual-windows --reanalyse --relaxed-prot-inf --smart-profiling --pg-level 1 --peak-center --no-ifs-removal"

import os


def generate_diann_command(folder, output_folder, fasta_file, threads=32, qvalue=0.01, min_fr_mz=200, max_fr_mz=1800,
                           min_pr_mz=300, max_pr_mz=1800, min_pr_charge=1, max_pr_charge=6, min_pep_len=6,
                           max_pep_len=32,
                           missed_cleavages=1):
    # Initialize the command with the executable and options
    command = 'diann.exe'

    # Add .raw files from the specified folder
    for file_name in os.listdir(folder):
        if file_name.endswith('.raw'):
            command += f' --f {os.path.join(folder, file_name)}'

    # Add other options
    command += f' --lib --threads {threads} --verbose 4 --out {os.path.join(output_folder, "report.tsv")}'
    command += f' --qvalue {qvalue} --matrices --out-lib {os.path.join(output_folder, "report-lib.tsv")}'
    command += f' --gen-spec-lib --predictor --fasta {fasta_file} --fasta-search'
    command += f' --min-fr-mz {min_fr_mz} --max-fr-mz {max_fr_mz} --met-excision --cut K*,R*'
    command += f' --missed-cleavages {missed_cleavages} --min-pep-len {min_pep_len} --max-pep-len {max_pep_len}'
    command += f' --min-pr-mz {min_pr_mz} --max-pr-mz {max_pr_mz} --min-pr-charge {min_pr_charge} --max-pr-charge {max_pr_charge}'
    command += f' --unimod4 --var-mods 1 --double-search --individual-mass-acc --individual-windows --reanalyse'
    command += f' --relaxed-prot-inf --smart-profiling --pg-level 1 --peak-center --no-ifs-removal'

    return command


# Example usage
folder = r'C:\Users\onur.serce\Downloads\2024May_Onur'
output_folder = r'C:\Users\onur.serce\Downloads\2024May_Onur\diann output main'
fasta_file = r'C:\Users\onur.serce\ownCloud - Onur Serce (onse)@datashare.mpcdf.mpg.de\UP000000589_10090.fasta'

command_string = generate_diann_command(folder, output_folder, fasta_file)
print(command_string)
