import pandas as pd

rainbow_segmentation = pd.read_json('/Users/onur.serce/Downloads/Rainbow 2017.json').set_index('index')

df = rainbow_segmentation

df[df['name'].str.contains('insula')]

# Write a function to ask which regions are there in the slice
# Needs rainbow segmentation mask of the section as an input (and the json look up table)
