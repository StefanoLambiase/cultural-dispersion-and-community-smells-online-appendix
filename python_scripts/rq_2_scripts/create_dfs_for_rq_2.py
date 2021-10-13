# Imports
import math

import numpy as np
import statistics

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

# ----------------------------------------

#create_projects_with_hofstede_df(gb.START_DF_PATH, gb.HOFSTEDE_DF_PATH, gb.PROJECT_WITH_HOFSTEDE_DF_PATH)
