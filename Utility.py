#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 08:43:52 2022

@author: onurserce

Utility functions
"""

import numpy as np
import pandas as pd
import os


def CreateTidyingTemplateFromPgMatrix(PgMatrix, OutputDirectory):
    """
    Given a DIANN protein groups output, create a template mapping.csv file.

    This template should be edited by the user. #Todo: Add instructions.
    """
    ColumnsSplitted = PgMatrix.columns.str.split("\\")
    NewNames = [e[-1] for e in ColumnsSplitted[4:]]
    Array = np.empty(shape=(len(NewNames)))
    Array[:] = np.nan

    TempDf = pd.DataFrame(index=PgMatrix.columns[4:],
                          columns=['ExperimentID', 'TextToColumnsWithExcel'])
    TempDf.index.name = 'OriginalName'
    TempDf['ExperimentID'] = Array
    TempDf['TextToColumnsWithExcel'] = NewNames

    if not os.path.exists(os.path.join(OutputDirectory, 'mapping.csv')):
        TempDf.to_csv(os.path.join(OutputDirectory, 'mapping.csv'))
        print(os.path.join(OutputDirectory, 'mapping.csv'), 'created!')
    else:
        raise Exception(
            os.path.join(OutputDirectory, 'mapping.csv') + ' already exists!')


def ImputeWithDownshift(df, shift=1.8, width=0.3):
    df_imp = df.copy()

    for column in df_imp.columns:

        mu = df_imp[column].mean()
        std = df_imp[column].std()

        for i in range(len(df_imp)):

            if df_imp[column][i] != df_imp[column][i]:
                df_imp[column][i] = np.random.normal(mu - shift * std, width * std, 1)

    return df_imp
