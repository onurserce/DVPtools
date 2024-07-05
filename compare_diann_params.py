import pandas as pd

old_params = r"--lib  --threads 32 --verbose 4 --out C:\Users\onur.serce\Downloads\2024May_Onur\diann output main\report.tsv --qvalue 0.01 --matrices --out-lib C:\Users\onur.serce\Downloads\2024May_Onur\diann output main\report-lib.tsv --gen-spec-lib --predictor --fasta C:\Users\onur.serce\ownCloud - Onur Serce (onse)@datashare.mpcdf.mpg.de\UP000000589_10090.fasta --fasta-search --min-fr-mz 200 --max-fr-mz 1800 --met-excision --cut K*,R* --missed-cleavages 1 --min-pep-len 6 --max-pep-len 32 --min-pr-mz 300 --max-pr-mz 1800 --min-pr-charge 1 --max-pr-charge 6 --unimod4 --var-mods 1 --double-search --individual-mass-acc --individual-windows --reanalyse --relaxed-prot-inf --smart-profiling --pg-level 1 --peak-center --no-ifs-removal"

old_params = old_params.split("--")
old_params = old_params[1:]
old_params_dict = {}
for old_param in old_params:
    splitted = old_param.split(" ")
    old_params_dict[splitted[0]] = " ".join(splitted[1:])

print(old_params_dict)

df = pd.DataFrame(data=old_params_dict.values(), index=old_params_dict.keys(), columns=['old'])

new_params = r"--lib --threads 32 --verbose 4 --out /u/onse/report.tsv --qvalue 0.01 --matrices --out-lib /u/onse/report-lib.tsv --gen-spec-lib --predictor --fasta /u/onse/data/UP000000589_10090.fasta --fasta-search --min-fr-mz 200 --max-fr-mz 1800 --met-excision --cut K*,R* --missed-cleavages 1 --min-pep-len 6 --max-pep-len 32 --min-pr-mz 300 --max-pr-mz 1800 --min-pr-charge 1 --max-pr-charge 6 --unimod4 --var-mods 1 --double-search --individual-mass-acc --individual-windows --reanalyse --relaxed-prot-inf --smart-profiling --pg-level 1 --peak-center --no-ifs-removal"
new_params = new_params.split("--")
new_params = new_params[1:]
new_params_dict = {}
for new_param in new_params:
    splitted = new_param.split(" ")
    new_params_dict[splitted[0]] = " ".join(splitted[1:])

print(new_params_dict)

for param in new_params_dict.keys():
    df.loc[param, 'new'] = new_params_dict[param]

for idx in df.index:
    if df.loc[idx, 'new'] == df.loc[idx, 'old']:
        df.loc[idx, 'bool'] = True
    else:
        df.loc[idx, 'bool'] = False