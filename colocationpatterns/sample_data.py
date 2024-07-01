import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point


def generate_sample_data():

    data = gpd.GeoDataFrame([
        {'instance_id': 1, 'spatial_feature_type': 'A', 'geometry': Point(1.75, 1.75)},
        {'instance_id': 2, 'spatial_feature_type': 'A', 'geometry': Point(5.45, 3.75)},
        {'instance_id': 3, 'spatial_feature_type': 'A', 'geometry': Point(8.5, 3.25)},
        {'instance_id': 4, 'spatial_feature_type': 'A', 'geometry': Point(4.25, 5)},
        {'instance_id': 1, 'spatial_feature_type': 'B', 'geometry': Point(2.1, 0.5)},
        {'instance_id': 2, 'spatial_feature_type': 'B', 'geometry': Point(10.65, 0.85)},
        {'instance_id': 3, 'spatial_feature_type': 'B', 'geometry': Point(13.74, 3.9)},
        {'instance_id': 4, 'spatial_feature_type': 'B', 'geometry': Point(6.25, 1.35)},
        {'instance_id': 5, 'spatial_feature_type': 'B', 'geometry': Point(15.1, 6)},
        {'instance_id': 1, 'spatial_feature_type': 'C', 'geometry': Point(8.65, 1)},
        {'instance_id': 2, 'spatial_feature_type': 'C', 'geometry': Point(0.1, 3.3)},
        {'instance_id': 3, 'spatial_feature_type': 'C', 'geometry': Point(14.2, 5.5)}
    ])

    return data


def plot_sample_data(sample_data: gpd.GeoDataFrame):

    fig, ax = plt.subplots(figsize=(10, 5))
    for category, data_category in sample_data.groupby(by='spatial_feature_type', as_index=False):
        data_category.plot(
            ax=ax,
            marker={'A': 'o', 'B': 's', 'C': '^'}.get(category),
            color={'A': 'blue', 'B': 'green', 'C': 'red'}.get(category),
            label=category
        )
    ax.legend()
    ax.set_title('Sample data spatial distribution')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_xlim([-1, 16])
    ax.set_ylim([0, 7])
    for row in sample_data.itertuples():
        ax.text(row.geometry.x+0.15, row.geometry.y+0.15, '.'.join([row.spatial_feature_type, str(row.instance_id)]))

    return fig, ax
