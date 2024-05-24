import numpy as np
import pandas as pd
from imageio.v2 import imread


print(df[df['name'].str.contains('insula')])


def get_segmented_regions(segmentation_mask, mapping_df):
    # Get unique colors in the segmentation mask
    unique_colors = np.unique(segmentation_mask.reshape(-1, segmentation_mask.shape[2]), axis=0)

    # Convert the unique colors to a DataFrame
    unique_colors_df = pd.DataFrame(unique_colors, columns=['red', 'green', 'blue'])

    # Merge the unique colors DataFrame with the mapping DataFrame to get the region names
    filtered_regions = pd.merge(unique_colors_df, mapping_df, on=['red', 'green', 'blue'], how='inner')

    return filtered_regions


# Example usage:
segmentation_mask = imread('atlas/example_brain/single_slice/brain_pr2_slide33-Rainbow_2017.png')
mapping_df = pd.read_json('atlas/example_brain/Rainbow 2017.json').set_index('index')

segmented_regions = get_segmented_regions(segmentation_mask, mapping_df)
print(segmented_regions)
