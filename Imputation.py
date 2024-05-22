#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 10:44:43 2022

@author: onurserce
"""

from IO import ReadPgMatrix
from tqdm import tqdm


def ImputeFromReplicates(PgMatrix, ThresholdRatio=0.66):
    """Imputation from replicates."""
    PgMatrix = PgMatrix.sort_index(axis=1)
    NaBeforeImputation = PgMatrix.isna()
    # Raise exception if the DataFrame doesn't have 'Replicates' column.
    if 'Replicate' not in PgMatrix.columns.names:
        raise Exception("'Replicate' column not found, aborting imputation!!!")

    ReplicateLevel = PgMatrix.columns.names.index('Replicate')
    Unique = PgMatrix.columns.droplevel(ReplicateLevel).unique()

    for U in tqdm(Unique,
                  desc="Imputing missing data using 'Replicate' averages"):
        Slice = PgMatrix.loc[:, U]  # Get the current group of replicates
        Averages = Slice.mean(axis=1)
        NReplicates = len(PgMatrix.loc[:, U].columns)  # Count of replicates
        OverThreshold = (
            Slice.notna().sum(axis=1) / NReplicates
            ) >= ThresholdRatio  # Check if the row is above the threshold
        Missing = Slice.isna().any(axis=1)  # Rows with missing values
        Impute = OverThreshold & Missing  # Impute boolean
        PgsToImpute = Impute[Impute == True].index  # Proteins to impute

        print(
            'Slice', U, ':',
            len(PgsToImpute), 'PGs will be imputed from replicates.')
        ImputedSlice = Slice.T.fillna(Averages.loc[PgsToImpute]).T
        PgMatrix.loc[:, U] = ImputedSlice.values  # Back into the DataFrame

    NaAfterImputation = PgMatrix.isna()
    ImputedBool = NaAfterImputation != NaBeforeImputation
    SkippedImputationBool = NaAfterImputation & NaBeforeImputation

    return PgMatrix, ImputedBool, SkippedImputationBool


def ImputeWithDownshift():
    """To be implemented."""
    pass


if __name__ == "__main__":
    import sys
    print("Initiating with args: ", sys.argv)