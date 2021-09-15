# Imports
import statistics

import pandas as pd
import numpy as np

from geopy.geocoders import Nominatim
from geopy import distance

# Custom imports
from python_scripts.globals import globals as gb


class CountryData:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


# Step 1 ---------------------------------------------------------------------------------------------------------------
def create_dfs_with_smells():
    lone_wolf_df = gb.get_smelly_df(gb.DF_WITH_LONE_WOLF_PATH)
    projects_with_hofstede_df = gb.get_projects_with_hofstede_df(gb.PROJECT_WITH_HOFSTEDE_DF_PATH)

    lone_wolf_columns = [
        'rowId', 'blauGender', 'turnover', 'lone', 'tenureMedian',
        'tenureDiversity', 'expertise', 'teamSize', 'stCongruence',
        'truckFactor', 'centrality', 'totalCommitters', 'female',
        'projectAge', 'totalcommits'
    ]
    lone_wolf_df = lone_wolf_df[lone_wolf_columns].copy()

    lone_wolf_df.rename(columns={'rowId': 'row_id'}, inplace=True)

    merged_df = pd.merge(
        lone_wolf_df, projects_with_hofstede_df,
        on='row_id'
    )

    merged_df = merged_df.sort_values(['project_id', 'window_idx'], ascending=[True, True])

    merged_df = add_geo_distance_to_df(merged_df)

    for index, row in merged_df.iterrows():
        if row['geo_distance'] == 0.00:
            countries = row['countries'].split(',')

            result = False
            if len(countries) > 0:
                result = all(elem == countries[0] for elem in countries)
            if result:
                print("All Elements in List are Equal")
                if countries[0] == 'None':
                    merged_df.loc[index, 'geo_distance'] = np.nan
            else:
                print("All Elements in List are Not Equal")

    merged_df.to_csv('../../data/df_with_geolocation/lone_with_geo_metrics.csv', sep=';', index=False)
    return merged_df


def add_geo_distance_to_df(df):
    geo_distance_list = list()
    x = 0
    for index, row in df.iterrows():
        print('PROGRESS: ' + str(x) + '/' + str(len(df.index)))
        x += 1
        countries = row['countries'].split(',')

        if len(countries) > 1:
            country_data_list = list()
            print(len(countries))
            for country in countries:
                if country != 'None':
                    country_data_list.append(get_country_data(country))

            print(len(country_data_list))
            if len(country_data_list) > 1:
                i = 0
                distances_list = list()

                while i != (len(country_data_list) - 1):
                    for j in range(i + 1, len(country_data_list)):
                        location_1 = country_data_list[i]
                        location_2 = country_data_list[j]

                        dis = calculate_geo_distance(location_1, location_2)

                        if not np.isnan(dis):
                            distances_list.append(round(dis, 2))
                    i += 1

                if len(distances_list) > 1:
                    geo_distance = statistics.stdev(distances_list)
                    geo_distance_list.append(geo_distance)
                else:
                    geo_distance_list.append(np.nan)
            else:
                geo_distance_list.append(np.nan)
        elif countries[0] == 'None':
            geo_distance_list.append(np.nan)
        else:
            geo_distance_list.append(0.0)

    df['geo_distance'] = geo_distance_list
    return df


def get_country_data(country):
    try:
        geolocator = Nominatim(user_agent="Stefano_thesis")
        location = geolocator.geocode(country)

        return CountryData(location.latitude, location.longitude)
    except Exception as e:
        print("An exception occurred: ", e)
        return


def calculate_geo_distance(location_1, location_2):
    try:
        dis = distance.distance(
            (location_1.latitude, location_1.longitude),
            (location_2.latitude, location_2.longitude)
        ).miles

        return dis
    except Exception as e:
        print("An exception occurred: ", e)
        return np.nan


# Step 2 ---------------------------------------------------------------------------------------------------------------
def add_metrics_to_others_dfs():
    lone_complete_df = pd.read_csv('../../data/df_with_geolocation/lone_with_geo_metrics.csv', sep=';')
    lone_complete_df = lone_complete_df.sort_values(by='row_id', ascending=False)

    black_df = gb.get_smelly_df(gb.DF_WITH_BLACK_CLOUD_PATH)
    organisation_df = gb.get_smelly_df(gb.DF_WITH_ORGANISATION_SILO_PATH)
    radio_df = gb.get_smelly_df(gb.DF_WITH_RADIO_SILENCE_PATH)

    black_df = merge_dfs(black_df, 'black')
    organisation_df = merge_dfs(organisation_df, 'organisation')
    radio_df = merge_dfs(radio_df, 'radio')

    black_df['geo_distance'] = lone_complete_df['geo_distance']
    organisation_df['geo_distance'] = lone_complete_df['geo_distance']
    radio_df['geo_distance'] = lone_complete_df['geo_distance']

    black_df.to_csv('../../data/df_with_geolocation/black_with_geo_metrics.csv', sep=';', index=False)
    organisation_df.to_csv('../../data/df_with_geolocation/organisation_with_geo_metrics.csv', sep=';', index=False)
    radio_df.to_csv('../../data/df_with_geolocation/radio_with_geo_metrics.csv', sep=';', index=False)


def merge_dfs(df, measure):
    projects_with_hofstede_df = gb.get_projects_with_hofstede_df(gb.PROJECT_WITH_HOFSTEDE_DF_PATH)
    columns = [
        'rowId', 'blauGender', 'turnover', measure, 'tenureMedian',
        'tenureDiversity', 'expertise', 'teamSize', 'stCongruence',
        'truckFactor', 'centrality', 'totalCommitters', 'female',
        'projectAge'
    ]
    df = df[columns].copy()

    merged_df = pd.merge(
        df, projects_with_hofstede_df,
        left_on='rowId', right_on='row_id'
    )

    cols = merged_df.columns.tolist()
    cols.pop(0)
    cols = cols[14:25] + cols[0:14] + cols[25:]
    merged_df = merged_df[cols]

    merged_df = merged_df.sort_values(by='row_id', ascending=False)
    return merged_df


# Step 3 ---------------------------------------------------------------------------------------------------------------
def add_cultural_classical_distance():
    add_classical_cultural_distance(
        '../../data/df_with_geolocation/lone_with_geo_metrics.csv',
        '../../data/df_with_cultural/lone.csv'
    )

    add_classical_cultural_distance(
        '../../data/df_with_geolocation/black_with_geo_metrics.csv',
        '../../data/df_with_cultural/black.csv'
    )

    add_classical_cultural_distance(
        '../../data/df_with_geolocation/organisation_with_geo_metrics.csv',
        '../../data/df_with_cultural/organisation.csv'
    )

    add_classical_cultural_distance(
        '../../data/df_with_geolocation/radio_with_geo_metrics.csv',
        '../../data/df_with_cultural/radio.csv'
    )


def add_classical_cultural_distance(df_path, where_to_save_path):
    df = pd.read_csv(df_path, sep=';')

    for index, row in df.iterrows():
        print('PROGRESS: ' + str(index) + '/' + str(len(df.index)))

        hofstede_measures = gb.HOFSTEDE_INDEX_LIST

        for measure in hofstede_measures:
            if not isinstance(row[measure + '_values'], float):
                values = row[measure + '_values'].split(',')

                if len(values) > 1:
                    i = 0
                    distances_list = list()

                    while i != (len(values) - 1):
                        for j in range(i + 1, len(values)):
                            first_value = int(values[i])
                            second_value = int(values[j])

                            distances_list.append(abs(first_value - second_value))
                        i += 1

                    if len(distances_list) > 1:
                        df.loc[index, measure + '_distance'] = statistics.stdev(distances_list)
                else:
                    df.loc[index, measure + '_distance'] = 0.0
            else:
                print(row[measure + '_values'])
                df.loc[index, measure + '_distance'] = np.nan

    df.to_csv(where_to_save_path, sep=';', index=False)


# Execution ------------------------------------------------------------------------------------------------------------
df = create_dfs_with_smells()
add_metrics_to_others_dfs()
