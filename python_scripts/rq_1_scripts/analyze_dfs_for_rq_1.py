import statistics

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

# Custom imports
from python_scripts.globals import globals as gb


def generate_df_with_others(
        countries_with_stats_df_path,
        percentage_for_exclusion_threshold
):
    countries_with_stats_df = pd.read_csv(
        countries_with_stats_df_path,
        sep=','
    )

    countries_with_stats_df = countries_with_stats_df.sort_values('percentages', ascending=False)

    # Divide df into two dfs based on percentage threshold
    countries_above_threshold = \
        countries_with_stats_df[countries_with_stats_df['percentages'] >= percentage_for_exclusion_threshold]

    countries_below_threshold = \
        countries_with_stats_df[countries_with_stats_df['percentages'] < percentage_for_exclusion_threshold]

    # Create the 'others' row
    below_devs = sum(countries_below_threshold['number_of_devs'])
    below_percentage = sum(countries_below_threshold['percentages'])

    new_row = pd.DataFrame(
        data={
            'countries': ['others'],
            'number_of_devs': [below_devs],
            'percentages': [below_percentage]
        }
    )

    # Adds the 'others' row to the df
    new_df = pd.concat([countries_above_threshold, new_row])
    return new_df


def print_countries_plots(countries_with_stats_df_path, percentage_for_exclusion_threshold=0.01):
    if percentage_for_exclusion_threshold != 0.00:
        country_df = generate_df_with_others(countries_with_stats_df_path, percentage_for_exclusion_threshold)
    else:
        country_df = pd.read_csv(
            countries_with_stats_df_path,
            sep=','
        )

    colors = [
        '#1F77B4', '#FF7F0E', '#2CA02C',
        '#D62728', '#9467BD', '#8C564B',
        '#E377C2', '#7F7F7F', '#BCBD22',
        '#99CBFF'
    ]

    # Pie Plot -------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(7, 7))

    ax1.pie(
        country_df['number_of_devs'],
        labels=list(map(str.title, country_df['countries'])),
        colors=colors,
        autopct=lambda pct: ('%.0f' % pct) + '%' if pct >= 1.5 else '',
        shadow=False,
        startangle=90
    )

    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.suptitle('Pie chart for number of developers per country')

    ax1.axis('equal')
    plt.tight_layout()

    plt.savefig(gb.FIGURES_PATH + 'number_developers_per_country_pie.png', transparent=True)

    plt.show()

    # Barh Plot -------------------------------------------
    fig, ax = plt.subplots(figsize=(14, 7))

    # Horizontal Bar Plot
    ax.barh(
        list(map(str.title, country_df['countries'])), country_df['number_of_devs'],
        color=colors
    )

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=10)

    # Add x, y gridlines
    ax.grid(
        b=True, color='grey',
        linestyle='-.', linewidth=0.75,
        alpha=0.5
    )

    # Show top values
    # ax.invert_yaxis()

    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width() + 0.2, i.get_y() + 0.5,
                 str(round((i.get_width()), 2)),
                 fontsize=10, fontweight='bold',
                 color='black')

    # Add Plot Title
    plt.suptitle('Bar chart for number of developers per country')

    ax.set_xlabel("Number of developers", fontsize=12)

    plt.savefig(gb.FIGURES_PATH + 'number_developers_per_country_barh.png', transparent=True)
    # Show Plot
    plt.show()


def calculate_hofstede_metrics_for_all_github(devs_with_hofstede_df_path):
    df = pd.read_csv(devs_with_hofstede_df_path)
    hofstede_index_list = gb.HOFSTEDE_INDEX_LIST
    df_to_show = pd.DataFrame(hofstede_index_list, columns=['indexes'])

    mean_values = list()
    stdev_values = list()
    for hofstede_index in hofstede_index_list:
        index_values = df[hofstede_index].dropna().values

        index_mean = round(statistics.mean(index_values), 2)
        index_stdev = round(statistics.stdev(index_values), 2)

        mean_values.append(index_mean)
        stdev_values.append(index_stdev)

    df_to_show['mean'] = mean_values
    df_to_show['stdev'] = stdev_values

    return df_to_show


def print_boxplot_for_hofstede_metrics(devs_with_hofstede_df_path):
    x_ticks_list = [
        'Power\nDistance', 'Individualism', 'Masculinity', 'Uncertainty\nAvoidance',
        'Long Term\nOrientation', 'Indulgence'
    ]

    df = pd.read_csv(devs_with_hofstede_df_path)

    pdi_list = df['pdi'].dropna()
    idv_list = df['idv'].dropna()
    mas_list = df['mas'].dropna()
    uai_list = df['uai'].dropna()
    ltowvs_list = df['ltowvs'].dropna()
    ivr_list = df['ivr'].dropna()

    # Violin plot ---------------------------------------
    fig, ax = plt.subplots(figsize=(10, 8))
    violin_parts = ax.violinplot(
        [pdi_list, idv_list, mas_list, uai_list, ltowvs_list, ivr_list],
        showmedians=True,
        showmeans=True,
        showextrema=True,
    )

    # Modify colors for mean and medians:
    violin_parts['cmedians'].set_edgecolor('#ff2222')
    violin_parts['cmeans'].set_edgecolor('#008000')

    # Add x, y gridlines
    ax.grid(
        b=True, color='grey',
        linestyle='-.', linewidth=0.75,
        alpha=0.5
    )

    legend_elements = [
        Line2D([0], [0], color='#ff2222', lw=4, label='Medians'),
        Line2D([0], [0], color='#008000', lw=4, label='Average')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    ax.set_xticks([1, 2, 3, 4, 5, 6])
    ax.set_xticklabels(x_ticks_list)
    ax.set_ylabel('Hofstede measure value', fontsize=14)
    plt.suptitle('Violin plots for developers culture per Hofstede measure')
    plt.xticks(rotation=45)

    plt.savefig(gb.FIGURES_PATH + 'Hofstede_per_developers_violin.png', transparent=True)
    plt.show()

    # Box plot ----------------------------------------
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.boxplot(
        [pdi_list, idv_list, mas_list, uai_list, ltowvs_list, ivr_list],
        medianprops=dict(color='#ff2222')
    )

    # Add x, y gridlines
    ax.grid(
        b=True, color='grey',
        linestyle='-.', linewidth=0.75,
        alpha=0.5
    )

    legend_elements = [
        Line2D([0], [0], color='#ff2222', lw=4, label='Medians')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    ax.set_xticks([1, 2, 3, 4, 5, 6])
    ax.set_xticklabels(x_ticks_list)
    ax.set_ylabel('Hofstede measure value', fontsize=14)

    plt.suptitle('Box plots for developers culture per Hofstede measure')
    plt.xticks(rotation=45)

    plt.savefig(gb.FIGURES_PATH + 'Hofstede_per_developers_box.png', transparent=True)

    plt.show()


def calculate_hofstede_summary_stats_for_devs(devs_with_hofstede_df_path):
    df = pd.read_csv(devs_with_hofstede_df_path)

    pdi_list = df['pdi'].dropna()
    idv_list = df['idv'].dropna()
    mas_list = df['mas'].dropna()
    uai_list = df['uai'].dropna()
    ltowvs_list = df['ltowvs'].dropna()
    ivr_list = df['ivr'].dropna()

    first_row = [
        statistics.mean(pdi_list),
        statistics.mean(idv_list),
        statistics.mean(mas_list),
        statistics.mean(uai_list),
        statistics.mean(ltowvs_list),
        statistics.mean(ivr_list)
    ]

    first_row = np.round(first_row, decimals=3)

    second_row = [
        statistics.stdev(pdi_list),
        statistics.stdev(idv_list),
        statistics.stdev(mas_list),
        statistics.stdev(uai_list),
        statistics.stdev(ltowvs_list),
        statistics.stdev(ivr_list)
    ]

    second_row = np.round(second_row, decimals=3)

    new_df = pd.DataFrame(
        np.array([first_row, second_row]),
        columns=['pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']
    )

    return new_df


# Execution ------------------------------------------------------------------------------------------------------------

DEVS_WITH_HOFSTEDE_DF_PATH = gb.DEVS_WITH_HOFSTEDE_DF_PATH
COUNTRIES_WITH_STATS_DF_PATH = gb.COUNTRIES_WITH_STATS_DF_PATH


print_countries_plots(COUNTRIES_WITH_STATS_DF_PATH)
hofstede_stats_on_github_df = calculate_hofstede_metrics_for_all_github(DEVS_WITH_HOFSTEDE_DF_PATH)
print_boxplot_for_hofstede_metrics(DEVS_WITH_HOFSTEDE_DF_PATH)

df = calculate_hofstede_summary_stats_for_devs(DEVS_WITH_HOFSTEDE_DF_PATH)
