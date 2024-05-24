import numpy as np
import pandas as pd
from imageio.v2 import imread


def get_segmented_regions(segmentation_mask: np.ndarray, mapping_df: pd.DataFrame) -> pd.DataFrame:
    """
    Get a filtered DataFrame of regions present in the segmentation mask image.

    Args:
    segmentation_mask (np.ndarray): A color-coded segmentation mask image.
    mapping_df (pd.DataFrame): A DataFrame containing the mapping of RGB values to region names.

    Returns:
    pd.DataFrame: A filtered DataFrame containing only the regions present in the segmentation mask.
    """
    # Get unique colors in the segmentation mask
    unique_colors = np.unique(segmentation_mask.reshape(-1, segmentation_mask.shape[2]), axis=0)

    # Convert the unique colors to a DataFrame
    unique_colors_df = pd.DataFrame(unique_colors, columns=['red', 'green', 'blue'])

    # Merge the unique colors DataFrame with the mapping DataFrame to get the region names
    segmented_regions = pd.merge(unique_colors_df, mapping_df, on=['red', 'green', 'blue'], how='inner')

    return segmented_regions


# Example usage:
example_segmentation_mask = imread('atlas/example_brain/single_slice/brain_pr2_slide33-Rainbow_2017.png')
df = pd.read_json('atlas/example_brain/Rainbow 2017.json').set_index('index')

segmented_regions = get_segmented_regions(example_segmentation_mask, df)
print(segmented_regions)


print(df[df['name'].str.contains('insula')])