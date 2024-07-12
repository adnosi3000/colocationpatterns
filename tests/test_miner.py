from numbers import Number

from pytest import fixture
from geopandas import GeoDataFrame

from colocationpatterns.sample_data import generate_sample_data
from colocationpatterns.miner import ColocationMiner


@fixture
def miner_from_geodataframe():

    sample_data = generate_sample_data()
    return ColocationMiner(sample_data, 'spatial_feature_type', 'instance_id', 2.95)


def test_miner_init(miner_from_geodataframe):

    # validate types
    assert isinstance(miner_from_geodataframe.data, GeoDataFrame)
    assert isinstance(miner_from_geodataframe.feature_type_column, str)
    assert isinstance(miner_from_geodataframe.feature_type_unique_id_column, str)
    assert isinstance(miner_from_geodataframe.ET, set)
    assert isinstance(miner_from_geodataframe.R, Number)
    assert isinstance(miner_from_geodataframe.K, Number)
    assert isinstance(miner_from_geodataframe.tables, dict)

    # validate values based on sample data
    assert miner_from_geodataframe.feature_type_column == 'spatial_feature_type'
    assert miner_from_geodataframe.feature_type_unique_id_column == 'instance_id'
    assert miner_from_geodataframe.ET == {'A', 'B', 'C'}
    assert miner_from_geodataframe.R == 2.95
    assert miner_from_geodataframe.K == 3
    assert miner_from_geodataframe.tables == {1: {}, 2: {}, 3:{}}

    