# Imports
import math

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import statistics

# Custom imports

from python_scripts.globals import globals as gb


def get_hofstede_values_for_community(measure, project_with_hofstede_df, none_countries_exclusion_threshold=0.0):
    grouped = project_with_hofstede_df.groupby(project_with_hofstede_df.project_id, sort=False)

    supreme_count = 0
    average_measure_values = list()
    stdev_measure_values = list()

    idx = 0
    for element in grouped:
        print('create_devs_with_hofstede_df PROGRESS: ' + str(idx) + '/' + str(len(grouped)), end='\r')
        idx += 1

        df = element[1]
        stdev_values = df[measure + '_stdev']
        average_values = df[measure + '_average']
        countries_values_for_idx = df['countries']

        country_flag = False
        for countries_values in countries_values_for_idx:
            countries = countries_values.split(',')
            none_count = countries.count('None')

            if not none_count / len(countries) >= none_countries_exclusion_threshold:
                country_flag = False
                break
            else:
                country_flag = True

        if country_flag:
            count = 0
            for value in stdev_values:
                if not math.isnan(value):
                    count += 1

            if count / len(stdev_values) >= 0.75:
                supreme_count += 1
                average_measure_values.append(statistics.mean(average_values.dropna()))
                stdev_measure_values.append(statistics.mean(stdev_values.dropna()))

    print(len(grouped))
    print(supreme_count)

    return average_measure_values, stdev_measure_values


def show_plots_for_communities_cultural_dispersion(
        project_with_hofstede_df_path,
        none_countries_exclusion_threshold=0.0
):
    x_ticks_list = [
        'Power\nDistance', 'Individualism', 'Masculinity', 'Uncertainty\nAvoidance',
        'Long Term\nOrientation', 'Indulgence'
    ]

    project_with_hofstede_df = pd.read_csv(project_with_hofstede_df_path, sep=';')

    pdi_average_list, pdi_stedv_list = get_hofstede_values_for_community(
        'pdi', project_with_hofstede_df, none_countries_exclusion_threshold)
    idv_average_list, idv_stedv_list = get_hofstede_values_for_community(
        'idv', project_with_hofstede_df, none_countries_exclusion_threshold)
    mas_average_list, mas_stedv_list = get_hofstede_values_for_community(
        'mas', project_with_hofstede_df, none_countries_exclusion_threshold)
    uai_average_list, uai_stedv_list = get_hofstede_values_for_community(
        'uai', project_with_hofstede_df, none_countries_exclusion_threshold)
    ltowvs_average_list, ltowvs_stedv_list = get_hofstede_values_for_community(
        'ltowvs', project_with_hofstede_df, none_countries_exclusion_threshold)
    ivr_average_list, ivr_stedv_list = get_hofstede_values_for_community(
        'ivr', project_with_hofstede_df, none_countries_exclusion_threshold)

    # Violin plot for average ---------------------------------------
    fig, ax = plt.subplots(figsize=(10, 8))
    violin_parts = ax.violinplot(
        [pdi_average_list, idv_average_list, mas_average_list, uai_average_list, ltowvs_average_list, ivr_average_list],
        showmeans=True,
        showmedians=True,
        showextrema=True,

    )

    # Customize mean and median
    violin_parts['cmedians'].set_edgecolor('#ff2222')
    violin_parts['cmedians'].set_linestyle('dashed')
    violin_parts['cmeans'].set_edgecolor('#008000')
    violin_parts['cmeans'].set_linestyle('solid')

    # Add x, y gridlines
    ax.grid(
        b=True, color='grey',
        linestyle='-.', linewidth=0.75,
        alpha=0.5,
    )

    legend_elements = [
        Line2D([0], [0], color='#ff2222', lw=1, label='Medians', linestyle='dashed'),
        Line2D([0], [0], color='#008000', lw=1, label='Average', linestyle='solid')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    ax.set_xticks([1, 2, 3, 4, 5, 6])
    ax.set_xticklabels(x_ticks_list)
    ax.set_ylabel('Cultural average value', fontsize=14)

    plt.suptitle('Violin plots for communities cultural average per Hofstede measure')

    plt.xticks(rotation=45)

    plt.savefig(gb.FIGURES_PATH + 'communities_cultural_average_violin.png', transparent=True)
    plt.show()

    # Violin plot for stdev ---------------------------------------
    fig, ax = plt.subplots(figsize=(10, 8))
    violin_parts = ax.violinplot(
        [pdi_stedv_list, idv_stedv_list, mas_stedv_list, uai_stedv_list, ltowvs_stedv_list, ivr_stedv_list],
        showmeans=True,
        showmedians=True,
        showextrema=True,
    )

    # Customize mean and median
    violin_parts['cmedians'].set_edgecolor('#ff2222')
    violin_parts['cmedians'].set_linestyle('dashed')
    violin_parts['cmeans'].set_edgecolor('#008000')
    violin_parts['cmeans'].set_linestyle('solid')

    # Add x, y gridlines
    ax.grid(
        b=True, color='grey',
        linestyle='-.', linewidth=0.75,
        alpha=0.5
    )

    legend_elements = [
        Line2D([0], [0], color='#ff2222', lw=1, label='Medians', linestyle='dashed'),
        Line2D([0], [0], color='#008000', lw=1, label='Average', linestyle='solid')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    ax.set_xticks([1, 2, 3, 4, 5, 6])
    ax.set_xticklabels(x_ticks_list)
    ax.set_ylabel('Cultural dispersion value', fontsize=14)

    plt.suptitle('Violin plots for communities cultural dispersion per Hofstede measure')
    plt.xticks(rotation=45)

    plt.savefig(gb.FIGURES_PATH + 'communities_cultural_dispersion_violin.png', transparent=True)
    plt.show()


# ----------------------------------------------------------------------------------------------------------------------

show_plots_for_communities_cultural_dispersion(gb.PROJECT_WITH_HOFSTEDE_DF_PATH, 0.5)
