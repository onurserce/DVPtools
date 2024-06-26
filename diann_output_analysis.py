import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from IO import ReadPgMatrix
from Imputation import ImputeFromReplicates

plt.rcParams['figure.dpi'] = 150

# Ran the TidyPgMatrix.py file first

PgMatrix = ReadPgMatrix("/Users/onur.serce/Data/MPIB/20240326_backup_slides/TidyPgMatrix.csv", header=[0, 1])

detected_prot_groups = PgMatrix.count(axis=0)
detected_prot_groups = pd.DataFrame(detected_prot_groups, columns=['detected_prot_groups']).reset_index().astype(int)

sb.boxplot(data=detected_prot_groups, x='Shapes', y='detected_prot_groups')
sb.stripplot(data=detected_prot_groups, x='Shapes', y='detected_prot_groups', hue='Replicate')
plt.grid(axis="y", linestyle="--")
plt.ylim(0, 6000)
plt.show()

sb.scatterplot(data=detected_prot_groups, x='Shapes', y='detected_prot_groups', hue='Replicate',
               style='Replicate')  # Log-linear regression
plt.grid(axis="y", linestyle="--")
plt.ylim(0, 6000)
plt.show()

sb.barplot(data=detected_prot_groups, x='Shapes', y='detected_prot_groups', hue='Replicate')
plt.grid(axis="y", linestyle="--")
plt.ylim(0, 6000)
plt.show()

ImputedPgMatrix, ImputedBool, SkippedImputation = ImputeFromReplicates(PgMatrix=PgMatrix)

n_of_imputed = pd.DataFrame(ImputedBool.sum(axis=0), columns=['n_of_imputed']).reset_index().astype(int)

sb.barplot(data=n_of_imputed, x='Shapes', y='n_of_imputed', hue='Replicate')
plt.show()

sb.barplot(data=n_of_imputed, x='Shapes', y='n_of_imputed')
plt.show()

sb.barplot(data=n_of_imputed.groupby('Shapes').sum(), x='Shapes', y='n_of_imputed')
plt.show()

detected_prot_groups_after_imputation = ImputedPgMatrix.count(axis=0)
detected_prot_groups_after_imputation = pd.DataFrame(
    data=detected_prot_groups_after_imputation, columns=['detected_prot_groups']).reset_index().astype(int)

imputation_comparison = detected_prot_groups_after_imputation.rename(
    columns={'detected_prot_groups': 'PGs_after_imputation'}).set_index(['Shapes', 'Replicate'])

before_imputation = detected_prot_groups.set_index(['Shapes', 'Replicate'])

imputation_comparison = imputation_comparison.join(before_imputation, how='outer').rename(
    columns={'detected_prot_groups': 'PGs_before_imputation'})
imputation_comparison['difference'] = imputation_comparison['PGs_after_imputation'] - imputation_comparison[
    'PGs_before_imputation']

imp_comp = imputation_comparison.reset_index().melt(id_vars=['Shapes', 'Replicate'],
                                                    value_vars=['PGs_after_imputation', 'PGs_before_imputation',
                                                                'difference'],
                                                    value_name='n_PGs')

sb.barplot(data=imp_comp, x='Shapes', y='n_PGs', hue='variable')
plt.grid(axis="y", linestyle="--")
plt.ylim(0, 6000)
plt.show()

sb.lmplot(data=imp_comp, x='Shapes', y='n_PGs', hue='variable', logx=True)
plt.grid(axis="y", linestyle="--")
plt.ylim(0, 6000)
plt.show()

sb.lmplot(data=imp_comp.set_index("Shapes").drop([0, 25, 50]).reset_index(), x='Shapes', y='n_PGs', hue='variable',
          logx=True)
plt.grid(axis="y", linestyle="--")
plt.ylim(0, 6000)
plt.show()

import gseapy as gp

full_report = pd.read_csv('/Users/onur.serce/Data/MPIB/20240326_backup_slides/report.pg_matrix.tsv', sep='\t')

imputedPgMatrix_w_Genes = ImputedPgMatrix.loc[:, '1000'].join(full_report.set_index('Protein.Group')['Genes'],
                                                              how='left')

imputedGenesMatrix = imputedPgMatrix_w_Genes.set_index('Genes')

Genes_median = imputedGenesMatrix.median(1, skipna=False).dropna(how='any')
# ToDo: There are proteins without Gene names??? To debug, skip the following Na removal from the index...
Genes_median = Genes_median[Genes_median.index.notnull()]
Genes_median = pd.DataFrame(data=Genes_median, columns=['LFQ'])

for Pg in Genes_median.index.copy(deep=True):
    if len(Pg.split(';')) > 1:
        Genes_median.loc[Pg, 'Gene'] = Pg.split(';')[0]
    else:
        Genes_median.loc[Pg, 'Gene'] = Pg

Genes_median['Gene'].to_clipboard(index=False)

Genes_median['LFQ'] = (Genes_median['LFQ'] - Genes_median['LFQ'].min()) / Genes_median['LFQ'].max()
Genes_w_weights = [str(Genes_median.loc[entry, 'Gene'])+', '+f"{Genes_median.loc[entry, 'LFQ']:.18f}" for entry in Genes_median.index]
pd.Series(Genes_w_weights).to_clipboard(index=False)

# Are NeuN, Fos and Gad67 detected?
# NeuN = Q8BIF2
# Fos = P01101
# Gad67 = P48318

Q8BIF2 = np.log2(PgMatrix).loc['Q8BIF2'].drop(['0', '25'], level=0).reset_index()
P48318 = np.log2(PgMatrix).loc['P48318'].drop(['0', '25'], level=0).reset_index()
sb.barplot(data=Q8BIF2, x='Shapes', y='Q8BIF2')
plt.show()

neun_gad67 = np.log2(PgMatrix).loc[['Q8BIF2', 'P48318']].drop(['0', '25'], level=0, axis='columns').T
medians = np.log2(PgMatrix).drop(['0', '25'], level=0, axis='columns').T.median(1)
mins = np.log2(PgMatrix).drop(['0', '25'], level=0, axis='columns').T.min(1)
maxs = np.log2(PgMatrix).drop(['0', '25'], level=0, axis='columns').T.max(1)
neun_gad67['sample_min'] = mins
neun_gad67['sample_median'] = medians
neun_gad67['sample_max'] = maxs
neun_gad67.rename(columns={'Q8BIF2': 'NeuN', 'P48318': 'Gad67'}, inplace=True)

melted = neun_gad67.reset_index().melt(id_vars=['Shapes', 'Replicate'], value_name='Log2(exp)')

sb.set_palette('colorblind')

sb.boxplot(data=melted, x='Log2(exp)', y='Shapes', hue='Pg')
plt.legend(bbox_to_anchor=(0.65, 1), loc='upper left')
plt.grid(axis="x", linestyle="--")
plt.show()

np.log2(PgMatrix).drop(['0', '25'], level=0, axis='columns').T.groupby('Shapes').median()
