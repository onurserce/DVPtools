"""
Created on Sun Jun 26 13:27:26 2022

@author: onurserce
"""

import os
import pandas as pd
from IO import ReadPgMatrix
from Utility import CreateTidyingTemplateFromPgMatrix


# ToDo: Add replicate support & imputation


def TidyPgMatrixFromMappingFile(PgMatrix, MappingFilePath, OutputDirectory):
    """Tidy and save protein groups matrix using a mapping.csv file."""
    Mapping = pd.read_csv(MappingFilePath)

    # Create MultiIndex
    Categories = [c for c in Mapping.columns if
                  c != 'OriginalName' and c != 'ExperimentID']
    Arrays = [Mapping.loc[:, a] for a in Categories]
    MultiIndex = pd.MultiIndex.from_arrays(arrays=Arrays, names=Categories)
    PgMatrix = PgMatrix.drop(
        columns=[
            'Protein.Ids',
            'Protein.Names',
            'Genes',
            'First.Protein.Description'])
    PgMatrix.columns = MultiIndex
    PgMatrix.index.name = 'Pg'

    PgMatrix.to_hdf(os.path.join(OutputDirectory, 'TidyPgMatrix.hdf'),
                    key='TidyPgMatrix')
    PgMatrix.to_csv(os.path.join(OutputDirectory, 'TidyPgMatrix.csv'))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--PgMatrixFilePath', '-i', help='Path to the DiaNN PgMatrix file.')
    parser.add_argument('--OutputDirectory', '-o', default=None, help='Path to the output directory. Defaults to '
                                                                      'None, which will use the current directory.')
    args = parser.parse_args()

    print("Initiating with args: ", sys.argv)

    Path_PgMatrix = args.PgMatrixFilePath
    output_dir = os.path.split(Path_PgMatrix)[0]
    PgMatrix = ReadPgMatrix(Path_PgMatrix)

    if args.OutputDirectory:
        OutputDirectory = args.OutputDirectory

    try:
        CreateTidyingTemplateFromPgMatrix(
            PgMatrix=PgMatrix, OutputDirectory=output_dir)
        print('Please edit the mapping.csv file and re-run the script!')
        exit(0)
    except Exception:
        print(
            os.path.join(output_dir, 'mapping.csv'), 'found!',
            'Tidying the PgMatrix..')
        input_ = 'continue'

    if input_ == 'continue':
        MappingFilePath = os.path.join(output_dir, 'mapping.csv')
        TidyPgMatrixFromMappingFile(PgMatrix=PgMatrix,
                                    MappingFilePath=MappingFilePath,
                                    OutputDirectory=output_dir)
        print('Completed. Exiting script!')
        exit(0)
    else:
        print('Exiting script from the else statement! Please debug!')
        exit(0)
