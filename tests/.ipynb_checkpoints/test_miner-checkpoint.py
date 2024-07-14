from numbers import Number

from pytest import fixture, mark
from geopandas import GeoDataFrame
from pandas import DataFrame
from shapely.geometry import Point

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
    assert miner_from_geodataframe.statistics is None
    assert miner_from_geodataframe.colocations is None

    # validate values based on sample data
    assert miner_from_geodataframe.feature_type_column == 'spatial_feature_type'
    assert miner_from_geodataframe.feature_type_unique_id_column == 'instance_id'
    assert miner_from_geodataframe.ET == {'A', 'B', 'C'}
    assert miner_from_geodataframe.R == 2.95
    assert miner_from_geodataframe.K == 3
    assert miner_from_geodataframe.tables == {2: {}, 3:{}}
    assert miner_from_geodataframe.statistics is None
    assert miner_from_geodataframe.colocations is None


@mark.parametrize('test_table', [
    DataFrame([
        {'B': 1, 'A': 1, 'geometry': None},
        {'B': 4, 'A': 2, 'geometry': None},
        {'B': 4, 'A': 3, 'geometry': None}
    ]),
    DataFrame([
        {'C': 1, 'A': 1, 'geometry': None},
        {'C': 2, 'A': 2, 'geometry': None},
        {'C': 5, 'A': 3, 'geometry': None},
        {'C': 7, 'A': 3, 'geometry': None},
        {'C': 2, 'A': 4, 'geometry': None}
    ]),
    DataFrame(columns=['A', 'B'])
])
def test_calculate_participation_ratio(miner_from_geodataframe, test_table):

    out = miner_from_geodataframe.calculate_participation_ratio(test_table, 'A')
    assert isinstance(out, Number)
    assert 1 >= out >= 0
    assert out == test_table['A'].nunique()/4

@mark.parametrize('v', [(1, 2, 3), (-1, 0, 1), (0.1, 0.4, 0.3)])
def test_calculate_participation_index(miner_from_geodataframe, v):

    out = miner_from_geodataframe.calculate_participation_index(v)
    assert isinstance(out, Number)
    assert out == min(v)

@mark.parametrize('R', [1, 10, 15, 20])
def test_merge_by_neighbourhood(miner_from_geodataframe, R):

    miner_from_geodataframe.R = R
    out = miner_from_geodataframe.merge_by_neighbourhood(('A', 'B'))

    assert isinstance(out, GeoDataFrame) or (out is None)

    






















