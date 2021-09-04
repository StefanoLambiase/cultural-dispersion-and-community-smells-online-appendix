import pandas as pd

# Path vars
START_DF_PATH = '../../data/start_df.csv'
ALL_DEVS_DF_PATH = '../../data/github_analysis/all_devs.csv'
HOFSTEDE_DF_PATH = '../../data/hofstede_metrics/hofstede.csv'
DEVS_WITH_HOFSTEDE_DF_PATH = '../../data/github_analysis/devs_with_hofstede.csv'
COUNTRIES_WITH_STATS_DF_PATH = '../../data/github_analysis/countries_with_stats.csv'
PROJECT_WITH_HOFSTEDE_DF_PATH = '../../data/community_analysis/projects_with_hofstede.csv'

FIGURES_PATH = '../../figures/'


# Vars
HOFSTEDE_INDEX_LIST = ["pdi", "idv", "mas", "uai", "ltowvs", "ivr"]


def get_start_df(dataset_path_par):
    df = pd.read_csv(
        dataset_path_par,
        sep=';',
    )
    return df


def get_hofstede_df(dataset_path):
    df = pd.read_csv(
        dataset_path,
        sep=','
    )
    return df


def get_all_devs_df(dataset_path):
    df = pd.read_csv(
        dataset_path,
        sep=','
    )
    return df


def get_countries_with_stats_df(dataset_path):
    df = pd.read_csv(
        dataset_path,
        sep=','
    )
    return df


def get_devs_with_hofstede(dataset_path):
    df = pd.read_csv(
        dataset_path,
        sep=','
    )
    return df


def get_projects_with_hofstede_df(dataset_path):
    df = pd.read_csv(
        dataset_path,
        sep=';',
    )
    return df


def get_num_of_country_with_high_known_values(df_par):
    count = 0
    for index, row in df_par.iterrows():
        countries = row['countries'].split(',')
        num_of_countries = len(countries)

        num_of_countries_not_none = 0
        for element in countries:
            if element != 'None':
                num_of_countries_not_none += 1

        known_countries_ratio = num_of_countries_not_none / num_of_countries
        if known_countries_ratio >= 0.75:
            count += 1

    return count
