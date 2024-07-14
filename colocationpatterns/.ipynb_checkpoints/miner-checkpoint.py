from itertools import combinations

import pandas as pd
from shapely import intersection
from geopandas import GeoDataFrame, sjoin
from colocationpatterns.sample_data import generate_sample_data

class ColocationMiner:

    def __init__(
        self,
        data: GeoDataFrame,
        feature_type_column: str,
        feature_type_unique_id_column: str,
        neighbourhood: float
    ):

        self.data = data # all events instances (id, event tpy, location, other attributes)
        self.feature_type_column = feature_type_column # column to recognize event type
        self.feature_type_unique_id_column = feature_type_unique_id_column # column with id unique within event type
        self.ET = set(data[feature_type_column].unique()) # set of event types
        self.K = data[feature_type_column].nunique() # number of event types
        self.R = neighbourhood # radius to set euclidean, neighbourhood relation
        self.tables = {k: {} for k in range(2, self.K+1)} # structure to store tables based on size-k colocation
        self.statistics = None
        self.colocations = None

    def calculate_participation_ratio(self, candidate_table, feature_type):

        all_feature_types = len(self.get_elementary_table(feature_type))
        features_in_colocation = candidate_table[feature_type].nunique()

        return features_in_colocation/all_feature_types

    def calculate_participation_index(self, participation_ratios):

        return min(participation_ratios)

    def calculate_conditional_probalility(self):

        pass

    def get_elementary_table(self, feature_type):

        return GeoDataFrame([{
            feature_type: getattr(event, self.feature_type_unique_id_column),
            'geometry': event.geometry
        } for event in self.data[self.data[self.feature_type_column]==feature_type].itertuples()])

    def merge_by_neighbourhood(self, tables_id:tuple):
    
        result = self.get_elementary_table(tables_id[0])    
        result['geometry'] = result['geometry'].buffer(self.R)
        
        for table_id in tables_id[1::]:

            table = self.get_elementary_table(table_id)
            merged = sjoin(result, table)
            if merged.empty: return None
            merged.drop(columns='index_right', inplace=True)
            merged = pd.merge(merged, table, left_on=table_id, right_on=table_id)
            merged['geometry_y'] = merged['geometry_y'].buffer(self.R)
            merged['geometry'] = merged.apply(lambda row: intersection(row['geometry_x'], row['geometry_y']), axis=1)
            result = merged.drop(columns=['geometry_x', 'geometry_y'])
    
        return result
    
    
    def mine(self, min_participation_index: float, store_higher_lvl_tables:bool=False, verbose:bool=False):

        statistics = {}

        # Generate co-location candidates and compute statistics starting from lvl k=2
        for k in range(2, self.K+1):
            
            for colocation in combinations(self.ET, k):

                if verbose: print(f'Creating table k_level = {k} for tables {colocation}')
                table = self.merge_by_neighbourhood(colocation)
                if table is None:
                    if verbose: print(f'No points for co-location candidate {colocation} to match neighbourhood definition R={self.R}')
                    continue
                if store_higher_lvl_tables:
                    self.tables[k][colocation] = table
                
                statistics[colocation] = {'participation_ratios': {}}
                for feature_type in colocation:
                    pr = self.calculate_participation_ratio(table, feature_type)
                    statistics[colocation]['participation_ratios'][feature_type] = pr
                    if verbose: print(f'\tParticipation ratio for {feature_type} in colocation {colocation} is {pr}')
                
                pi = self.calculate_participation_index(statistics[colocation]['participation_ratios'].values())
                statistics[colocation]['participation_index'] = pi
                if verbose: print(f'\tParticipation index for colocation {colocation} is {pi}')

                statistics[colocation]['colocation'] = pi >= min_participation_index
    
        self.statistics = statistics
        self.colocations = list(filter(lambda key: self.statistics[key]['colocation'], self.statistics.keys()))

        return self.colocations