from itertools import combinations

import pandas as pd
from shapely import intersection
from geopandas import GeoDataFrame, sjoin
from colocationpatterns.sample_data import generate_sample_data

class ColocationMiner:

    def __init__(self, data: GeoDataFrame, feature_type_column: str, feature_type_unique_id_column: str, neighbourhood: float):

        self.data = data # all events instances (id, event tpy, location, other attributes)
        self.feature_type_column = feature_type_column # column to recognize event type
        self.feature_type_unique_id_column = feature_type_unique_id_column # column with id unique within event type
        self.ET = set(data[feature_type_column].unique()) # set of event types
        self.R = neighbourhood # max distance to consider neighbour as colocation
        self.K = data[feature_type_column].nunique() # number of event types
        # self.table_ids_iterator = iter(range(0, sum(((factorial(self.K))//(factorial(i)*factorial(self.K-i)) for i in range(1, self.K+1)))))
        self.tables = {k: {} for k in range(1, self.K+1)} # structure to store tables based on size-k colocation

    def calculate_participation_ratio(self, colocation, feature_type, k):

        all_feature_types = len(self.tables[1][feature_type])
        colocation_table = self.tables[k][colocation]
        if colocation_table is None:
            return None
        features_in_colocation = colocation_table[feature_type].nunique()

        return features_in_colocation/all_feature_types

    def calculate_participation_index(self, participation_ratios):

        return min(participation_ratios)

    def calculate_conditional_probalility(self):

        pass

    def merge_by_neighbourhood(self, tables_id:tuple):

        result = cm.tables[1][tables_id[0]].copy()
        result['geometry'] = result['geometry'].buffer(self.R)
        
        for table_id in tables_id[1::]:
        
            table = cm.tables[1][table_id].copy()
            merged = sjoin(result, table)
            if merged.empty: return None
            merged.drop(columns='index_right', inplace=True)
            merged = pd.merge(merged, table, left_on=table_id, right_on=table_id)
            merged['geometry_y'] = merged['geometry_y'].buffer(self.R)
            merged['geometry'] = merged.apply(lambda row: intersection(row['geometry_x'], row['geometry_y']), axis=1)
            result = merged.drop(columns=['geometry_x', 'geometry_y'])
    
        return result
    
    
    def __call__(self):

        # Generate co-location candidates and compute statistics
        for k in range(1, self.K+1):
            
            for colocation in combinations(self.ET, k):

                if k == 1: # elementary tables
                    print('Creating elementary tables')
                    self.tables[k] =  { table_id:
                        GeoDataFrame(
                            [{
                                table_id: getattr(event, self.feature_type_unique_id_column),
                                'geometry': event.geometry
                            } for event in table[[self.feature_type_unique_id_column, 'geometry']].itertuples()]
                        ) for table_id, table in self.data.groupby(by=self.feature_type_column, as_index=False)
                    }
                    break

                

                print(f'Creating table k_level = {k} for tables {colocation}')
                table = self.merge_by_neighbourhood(colocation)
                self.tables[k][colocation] = table
                if table is None:
                    continue
                prs = []
                for feature_type in colocation:
                    pr = self.calculate_participation_ratio(colocation, feature_type, k)
                    prs.append(pr)
                    print(f'\tParticipation ratio for {feature_type} in colocation {colocation} is {pr}')
                
                pi = self.calculate_participation_index(prs)
                print(f'\tParticipation index for colocation {colocation} is {pi}')
                