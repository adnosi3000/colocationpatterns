import pytest
from geopandas import GeoDataFrame

from colocationpatterns.sample_data import generate_sample_data


def test_generate_sample_data():

    data = generate_sample_data()

    assert isinstance(data, GeoDataFrame)
    assert data.crs is None
    assert len(data) == 12
    assert set(data.columns) == {'instance_id', 'spatial_feature_type', 'geometry'}
    assert set(data.instance_id.unique()) == {1, 2, 3, 4, 5}
    assert set(data.spatial_feature_type.unique()) == set('ABC')
