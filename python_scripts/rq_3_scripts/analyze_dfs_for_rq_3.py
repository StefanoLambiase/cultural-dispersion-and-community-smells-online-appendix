# Imports
import math

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import statistics

# Custom imports
from python_scripts.globals import globals as gb


class Project:
    def __init__(self, project_id, project_name, measure_mean_list, measure_stdev_list, measure):
        self.project_id = project_id
        self.project_name = project_name
        self.measure_mean_list = measure_mean_list
        self.measure_stdev_list = measure_stdev_list
        self.measure = measure


def show_plots_for_communities_cultural_dispersion(
        project_with_hofstede_df_path,
        none_countries_exclusion_threshold=0.0
):
    x_ticks_list = [
        'Power\nDistance', 'Individualism', 'Masculinity', 'Uncertainty\nAvoidance',
        'Long Term\nOrientation', 'Indulgence'
    ]

    project_with_hofstede_df = pd.read_csv(project_with_hofstede_df_path, sep=';')
    project_with_hofstede_df = project_with_hofstede_df.sort_values(by=['project_id', 'window_idx'])

    projects_with_pdi = get_hofstede_values_for_community(
        'pdi', project_with_hofstede_df, none_countries_exclusion_threshold)
    projects_with_idv = get_hofstede_values_for_community(
        'idv', project_with_hofstede_df, none_countries_exclusion_threshold)
    projects_with_mas = get_hofstede_values_for_community(
        'mas', project_with_hofstede_df, none_countries_exclusion_threshold)
    projects_with_uai = get_hofstede_values_for_community(
        'uai', project_with_hofstede_df, none_countries_exclusion_threshold)
    projects_with_ltowvs = get_hofstede_values_for_community(
        'ltowvs', project_with_hofstede_df, none_countries_exclusion_threshold)
    projects_with_ivr = get_hofstede_values_for_community(
        'ivr', project_with_hofstede_df, none_countries_exclusion_threshold)

    # the plot of the data
    """
    plot = create_plot_for_temporal_increment(get_top_project(projects_with_pdi))
    plot.savefig(gb.FIGURES_PATH + 'pdi.png', transparent=True)

    create_plot_for_temporal_increment(get_top_project(projects_with_idv))
    plot.savefig(gb.FIGURES_PATH + 'idv.png', transparent=True)

    create_plot_for_temporal_increment(get_top_project(projects_with_mas))
    plot.savefig(gb.FIGURES_PATH + 'mas.png', transparent=True)

    create_plot_for_temporal_increment(get_top_project(projects_with_uai))
    plot.savefig(gb.FIGURES_PATH + 'uai.png', transparent=True)

    create_plot_for_temporal_increment(get_top_project(projects_with_ltowvs))
    plot.savefig(gb.FIGURES_PATH + 'ltowvs.png', transparent=True)

    create_plot_for_temporal_increment(get_top_project(projects_with_ivr))
    plot.savefig(gb.FIGURES_PATH + 'ivr.png', transparent=True)
    """

    # Violin plot part
    threshold = 0.0
    average_pdi_list, stdev_pdi_list = \
        calculate_average_and_stdev_increments_per_project(get_top_project(projects_with_pdi, threshold))
    average_idv_list, stdev_idv_list = \
        calculate_average_and_stdev_increments_per_project(get_top_project(projects_with_idv, threshold))
    average_mas_list, stdev_mas_list = \
        calculate_average_and_stdev_increments_per_project(get_top_project(projects_with_mas, threshold))
    average_uai_list, stdev_uai_list = \
        calculate_average_and_stdev_increments_per_project(get_top_project(projects_with_uai, threshold))
    average_ltowvs_list, stdev_ltowvs_list = \
        calculate_average_and_stdev_increments_per_project(get_top_project(projects_with_ltowvs, threshold))
    average_ivr_list, stdev_ivr_list = \
        calculate_average_and_stdev_increments_per_project(get_top_project(projects_with_ivr, threshold))

    projects_list_for_measure = [
        average_pdi_list, average_idv_list, average_mas_list, average_uai_list, average_ltowvs_list, average_ivr_list
    ]
    create_violinplot_for_temporal_increment(projects_list_for_measure)

    projects_list_for_measure = [
        stdev_pdi_list, stdev_idv_list, stdev_mas_list, stdev_uai_list, stdev_ltowvs_list, stdev_ivr_list
    ]
    create_violinplot_for_temporal_increment(projects_list_for_measure, average=False)

    return project_with_hofstede_df


def get_hofstede_values_for_community(measure, project_with_hofstede_df, none_countries_exclusion_threshold=0.0):
    grouped = project_with_hofstede_df.groupby(project_with_hofstede_df.project_id, sort=False)

    supreme_count = 0
    project_list = list()

    idx = 0
    for element in grouped:
        print('PROGRESS for ' + measure + ': ' + str(idx) + '/' + str(len(grouped)), end='\r')
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

        if country_flag and df['windows'].values[0] > 2:
            count = 0
            for value in stdev_values:
                if not math.isnan(value):
                    count += 1

            if count / len(stdev_values) >= 1:
                supreme_count += 1
                project = Project(
                    df['project_id'].values[0],
                    df['name'].values[0],
                    average_values.values,
                    stdev_values.values,
                    measure
                )
                project_list.append(project)

    print(len(grouped))
    print(supreme_count)

    return project_list


def get_top_project(projects_with_measure, threshold=0.7):
    top_measure_value_len = 0
    for project in projects_with_measure:
        if len(project.measure_stdev_list) > top_measure_value_len:
            top_measure_value_len = len(project.measure_stdev_list)

    top_projects_list = list()
    for project in projects_with_measure:
        if len(project.measure_stdev_list) >= (top_measure_value_len * threshold):
            top_projects_list.append(project)

    return top_projects_list


def create_plot_for_temporal_increment(top_projects_list):
    # the plot of the data
    plot = None
    for project in top_projects_list:
        print(project.project_name)
        plot = plt.plot(
            list(range(1, len(project.measure_stdev_list) + 1)),
            project.measure_stdev_list
        )

    plt.xlabel('Temporal windows')
    plt.ylabel('Measure value')
    plt.title(top_projects_list[0].measure)
    plt.grid(True)

    return plot


def calculate_average_and_stdev_increments_per_project(projects_with_measure):
    average_increments_list = list()
    stdev_increment_list = list()

    for project in projects_with_measure:
        measure_len = len(project.measure_stdev_list)
        measure_stdev_list = project.measure_stdev_list

        increments_list = list()
        i = 0
        while i < (measure_len - 1):
            first = measure_stdev_list[i]
            second = measure_stdev_list[i+1]
            increments_list.append(second - first)
            i += 1

        average = statistics.mean(increments_list)
        stdev = statistics.stdev(increments_list)

        average_increments_list.append(average)
        stdev_increment_list.append(stdev)

    return average_increments_list, stdev_increment_list


def create_violinplot_for_temporal_increment(projects_list_for_measure, average=True):
    x_ticks_list = [
        'Power\nDistance', 'Individualism', 'Masculinity', 'Uncertainty\nAvoidance',
        'Long Term\nOrientation', 'Indulgence'
    ]

    # Violin plot for stdev ---------------------------------------
    fig, ax = plt.subplots(figsize=(12, 8))
    violin_parts = ax.violinplot(
        projects_list_for_measure,
        showmeans=True,
        showmedians=True,
        showextrema=True,
        vert=False
    )

    # Make mean of the violin marks red:
    violin_parts['cmedians'].set_edgecolor('#ff2222')
    violin_parts['cmeans'].set_edgecolor('#008000')

    # Add x, y gridlines
    ax.grid(
        b=True, color='grey',
        linestyle='-.', linewidth=0.75,
        alpha=0.5
    )

    legend_elements = [
        Line2D([0], [0], color='#ff2222', lw=4, label='Median'),
        Line2D([0], [0], color='#008000', lw=4, label='Average')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    ax.set_yticks([1, 2, 3, 4, 5, 6])
    ax.set_yticklabels(x_ticks_list)
    ax.set_xlabel('Community cultural variation value' if average else 'Community cultural variation dispersion value',
                  fontsize=14)

    plt.suptitle('Communities cultural variations in time per Hofstede measure' if average
                 else 'Communities cultural variations dispersions in time per Hofstede measure')
    plt.yticks(rotation=45)

    if average:
        plt.savefig(gb.FIGURES_PATH + 'communities_cultural_variation_violin.png', transparent=True)
    else:
        plt.savefig(gb.FIGURES_PATH + 'communities_cultural_variation-dispersion_violin.png', transparent=True)
    plt.show()


project_with_hofstede_df = show_plots_for_communities_cultural_dispersion(gb.PROJECT_WITH_HOFSTEDE_DF_PATH, 0.5)
