# Imports
import pandas as pd
import numpy as np

# Custom imports
from python_scripts.globals import globals as gb


# Functions
def create_developers_df(start_df_path, to_save_path):
    start_df = pd.read_csv(
        start_df_path,
        sep=';',
    )

    all_devs = list()
    all_genders = list()
    all_countries = list()

    for index, row in start_df.iterrows():
        # Prints the progress
        print('Create developers df PROGRESS: ' + str(index) + '/' + str(len(start_df)), end='\r')

        # Gets all values
        devs = row['team'].split(',')
        genders = row['genders'].split(',')
        countries = row['countries'].split(',')

        # Iterates to eliminate None values
        idx_country = 0
        while idx_country < len(countries):
            if countries[idx_country] == 'None':
                del (devs[idx_country])
                del (genders[idx_country])
                del (countries[idx_country])
            else:
                idx_country += 1

        # Iterates to eliminate already inserted values
        idx_dev = 0
        while idx_dev < len(devs):
            if devs[idx_dev] in all_devs:
                del (devs[idx_dev])
                del (genders[idx_dev])
                del (countries[idx_dev])
            else:
                idx_dev += 1

        # Ads values to globals vars
        all_devs.extend(devs)
        all_genders.extend(genders)
        all_countries.extend(countries)

    print('COMPLETED')

    # Creates the df
    df = pd.DataFrame(
        list(zip(all_devs, all_genders, all_countries)),
        columns=['devs', 'genders', 'countries']
    )

    # Saves the df as csv
    df.to_csv(to_save_path)

    return df


def create_countries_with_stats_df(
        all_devs_df_path,
        to_save_path,
        percentage_for_exclusion_threshold=0.00
):
    # Gets the all devs dataset
    all_devs_df = pd.read_csv(
        all_devs_df_path,
        sep=','
    )

    # Calculate total number of devs
    total_number_of_devs = len(all_devs_df)
    exclusion_threshold = total_number_of_devs * percentage_for_exclusion_threshold

    # Create the country Series with number of developers excluding countries under threshold
    country_df = all_devs_df.countries.value_counts()
    country_df = country_df[country_df > exclusion_threshold]

    # Updates total number of devs
    total_number_of_devs = 0
    for devs in country_df.values:
        total_number_of_devs += devs

    # Calculate percentage
    percentages = list()
    for devs in country_df.values:
        percentage = devs / total_number_of_devs
        percentages.append(percentage)

    # Creates the df
    df = pd.DataFrame(
        list(zip(country_df.index, country_df.values, percentages)),
        columns=['countries', 'number_of_devs', 'percentages']
    )

    # Saves the df as csv
    df.to_csv(to_save_path)

    print('COMPLETED: create_countries_with_stats_df')
    return df


def create_devs_with_hofstede_df(
        all_devs_df_path,
        hofstede_df_path,
        to_save_path=''
):
    hofstede_index_list = ["pdi", "idv", "mas", "uai", "ltowvs", "ivr"]

    all_devs_df = pd.read_csv(
        all_devs_df_path,
        sep=","
    )

    hofstede_df = pd.read_csv(
        hofstede_df_path,
        sep=","
    )

    for hofstede_idx in hofstede_index_list:
        print(hofstede_idx)
        idx_values = list()

        for index, row in all_devs_df.iterrows():
            # Prints the progress
            print('create_devs_with_hofstede_df PROGRESS: ' + str(index) + '/' + str(len(all_devs_df)), end='\r')

            is_in_hofstede = False
            for index_2, row_2 in hofstede_df.iterrows():
                if row['countries'].lower() == row_2['country'].lower():
                    is_in_hofstede = True
                    idx_values.append(row_2[hofstede_idx])
                    break
            if not is_in_hofstede:
                idx_values.append(np.nan)

        # Using 'Address' as the column name and equating it to the list
        all_devs_df[hofstede_idx] = idx_values

        print(hofstede_idx + 'Ended')

    # Saves the df as csv
    all_devs_df.to_csv(to_save_path, index=False)

    return all_devs_df


def create_df_with_all_devs_in_start_df(start_df_path, to_save_path):
    start_df = pd.read_csv(
        start_df_path,
        sep=';',
    )

    all_devs = list()
    all_genders = list()
    all_countries = list()

    for index, row in start_df.iterrows():
        # Prints the progress
        print('Create all developers df PROGRESS: ' + str(index) + '/' + str(len(start_df)), end='\r')

        # Gets all values
        devs = row['team'].split(',')
        genders = row['genders'].split(',')
        countries = row['countries'].split(',')

        # Iterates to eliminate already inserted values
        idx_dev = 0
        while idx_dev < len(devs):
            if devs[idx_dev] in all_devs:
                del (devs[idx_dev])
                del (genders[idx_dev])
                del (countries[idx_dev])
            else:
                idx_dev += 1

        # Ads values to globals vars
        all_devs.extend(devs)
        all_genders.extend(genders)
        all_countries.extend(countries)

    print('COMPLETED')
    print('Number of devs: ' + str(len(all_devs)))

    # Creates the df
    df = pd.DataFrame(
        list(zip(all_devs, all_genders, all_countries)),
        columns=['devs', 'genders', 'countries']
    )

    # Saves the df as csv
    df.to_csv(to_save_path)

    return df


# --------------------

#create_countries_with_stats_df(gb.ALL_DEVS_DF_PATH, gb.COUNTRIES_WITH_STATS_DF_PATH)
#create_devs_with_hofstede_df(gb.ALL_DEVS_DF_PATH, gb.HOFSTEDE_DF_PATH, gb.DEVS_WITH_HOFSTEDE_DF_PATH)

create_df_with_all_devs_in_start_df(
    start_df_path=gb.START_DF_PATH,
    to_save_path=gb.ALL_DEVS_IN_START_DF_DF_PATH
)
