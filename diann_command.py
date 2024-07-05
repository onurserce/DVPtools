import os


def generate_diann_command(folder, output_folder, fasta_file, raw_file_format='.raw', threads=32, qvalue=0.01,
                           min_fr_mz=200, max_fr_mz=1800,
                           min_pr_mz=300, max_pr_mz=1800, min_pr_charge=1, max_pr_charge=6, min_pep_len=6,
                           max_pep_len=32,
                           missed_cleavages=1):
    # Initialize the command with the executable and options
    command = 'diann.exe'  # This is diann-1.8.1 on the HPC

    # Add .raw files from the specified folder
    for file_name in os.listdir(folder):
        if file_name.endswith(raw_file_format):
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
