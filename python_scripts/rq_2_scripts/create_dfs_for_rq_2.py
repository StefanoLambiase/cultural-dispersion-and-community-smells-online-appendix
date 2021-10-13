# Imports
import math

import numpy as np
import statistics

# Imports for geodispersion
from geopy.geocoders import Nominatim
from geopy import distance

from python_scripts.globals import globals as gb


# Functions
def create_projects_with_hofstede_df(
        start_df_path,
        hofstede_df_path,
        to_save_path=''
):
    # Gets the hofstede indexes
    hofstede_index_list = ["pdi", "idv", "mas", "uai", "ltowvs", "ivr"]

    # Gets the two dfs
    start_df = gb.get_start_df(start_df_path)
    hofstede_df = gb.get_hofstede_df(hofstede_df_path)

    start_df_columns = [
        'row_id', 'project_id', 'owner_login',
        'language', 'created_at', 'windows',
        'window_idx', 'name', 'team',
        'genders', 'countries'
    ]

    # Copies the columns from the start_df
    new_df = start_df[start_df_columns].copy()

    # Iterates to add hofstede metrics to each row
    for hofstede_idx in hofstede_index_list:
        print(hofstede_idx)
        idx_average_values = list()
        idx_stdev_values = list()
        idx_str_values = list()

        for index, row in new_df.iterrows():
            # Prints the progress
            percentage = round(index / len(new_df), 3)
            print('create_projects_with_hofstede_df PROGRESS for ' + hofstede_idx + ' :' + str(percentage), end='\r')

            idx_values = list()
            countries = row['countries'].split(',')
            countries = [i for i in countries if i != "None"]

            # Checks which country is in the hofstede df
            for country in countries:
                for index_2, row_2 in hofstede_df.iterrows():
                    if country.lower() == row_2['country'].lower():
                        idx_value = row_2[hofstede_idx]
                        if not math.isnan(idx_value):
                            idx_values.append(idx_value)
                        break

            # Calculates metrics on index values
            greater_than_two = len(idx_values) >= 2
            idx_row_values_average = statistics.mean(idx_values) if greater_than_two else np.nan
            idx_row_values_stdev = statistics.pstdev(idx_values) if greater_than_two else np.nan

            # Converts indexes list into a string
            idx_values = [int(x) for x in idx_values]
            idx_project_values_str = ','.join([str(x) for x in idx_values])

            idx_average_values.append(idx_row_values_average)
            idx_stdev_values.append(idx_row_values_stdev)
            idx_str_values.append(idx_project_values_str)

        # Adds the columns to the dataframe
        new_df[hofstede_idx + '_values'] = idx_str_values
        new_df[hofstede_idx + '_average'] = idx_average_values
        new_df[hofstede_idx + '_stdev'] = idx_stdev_values

        print(hofstede_idx + 'Ended')

    # Saves the df as csv
    new_df.to_csv(to_save_path, index=False, sep=";")

    return new_df


# Geo Dispersion part
class CountryData:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


def add_geo_dispersion_to_df():
    df =gb.get_projects_with_hofstede_df(gb.PROJECT_WITH_HOFSTEDE_DF_PATH)
    df = add_geo_distance_to_df(df)

    for index, row in df.iterrows():
        if row['geo_distance'] == 0.00:
            countries = row['countries'].split(',')

            result = False
            if len(countries) > 0:
                result = all(elem == countries[0] for elem in countries)
            if result:
                print("All Elements in List are Equal")
                if countries[0] == 'None':
                    df.loc[index, 'geo_distance'] = np.nan
            else:
                print("All Elements in List are Not Equal")

    df.to_csv('../../data/community_analysis/projects_with_cultural_and_geo_metrics.csv', sep=';', index=False)
    return df


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

# ----------------------------------------

#create_projects_with_hofstede_df(gb.START_DF_PATH, gb.HOFSTEDE_DF_PATH, gb.PROJECT_WITH_HOFSTEDE_DF_PATH)


add_geo_dispersion_to_df()
