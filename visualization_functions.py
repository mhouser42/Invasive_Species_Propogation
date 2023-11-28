"""
Functions used in our visualizations of the simulation
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
from run_simulation import infestation_main


def make_visual_df(simulation_df: pd.DataFrame) -> pd.DataFrame:
    """
    Utility function.
    rotates the run_simulation output df to help with some visualizations
    :param simulation_df:
    :return visual_df:
    """
    visual_df = simulation_df.T
    visual_df.columns = visual_df.iloc[0]
    visual_df = visual_df.drop(visual_df.index[0])
    return visual_df


def make_network_heat(CG, simulation_df, handler, month: int):
    """
    Makes a heatmap from the NX nodes, edges, and object instances
    :param CG:
    :param handler:
    :param simulation_df:
    :param month: The number of months from the interactive ipywidget
    """
    month = f'month {month}'
    #     min_value = simulation_df[month].min()
    #     max_value = simulation_df[month].max()  # This makes the scale variable for each chart
    max_value = 1  # This keeps the scale constant
    min_value = 0
    cmap = matplotlib.colormaps['YlOrRd']

    node_colors = {}
    for node in CG.nodes():
        value = simulation_df.loc[simulation_df['County'] == node.name, month].iloc[0]
        normalized_value = (value - min_value) / (max_value - min_value)
        node_colors[node.name] = cmap(normalized_value)

    labels = {node: handler[node.name].name for node in CG.nodes()}
    fig, ax = plt.subplots(figsize=(10, 15))
    node_positions = {node: [node.centroid.x, node.centroid.y] for node in CG.nodes()}
    nx.draw(CG,
            pos=node_positions,
            ax=ax,
            node_color=[node_colors.get(node.name, 'gray') for node in CG.nodes()],
            node_size=1500, )

    nx.draw_networkx_labels(CG,
                            pos=node_positions,
                            labels=labels,
                            font_size=6,
                            ax=ax,
                            font_color='k')

    edge_colors = ['gray' if CG[src][tgt]['rel'] == 'interstate' else 'gray' for src, tgt in CG.edges()]
    edge_widths = [5 if CG[src][tgt]['rel'] == 'interstate' else 1 for src, tgt in CG.edges()]
    nx.draw_networkx_edges(CG, pos=node_positions, edge_color=edge_colors, ax=ax, width=edge_widths)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min_value, vmax=max_value))
    sm.set_array([])
    sub_ax = plt.axes([0.96, 0.55, 0.02, 0.3])
    plt.colorbar(sm, cax=sub_ax)
    plt.show()


def make_average_graphs(df: pd.DataFrame, sim_months: int):
    """
    Takes the average values over the whole state for each given simulation df.
    Plots them all within the same graph
    :param df:
    :param sim_months:
    """
    vis_df = make_visual_df(df)
    avg_df = vis_df.mean(axis=1)
    plt.xticks(ticks=range(0, sim_months + 1),
               labels=range(0, sim_months + 1))
    plt.xlabel('Months')
    plt.ylabel('Infestation Percentage')
    plt.plot(avg_df.index, avg_df, linewidth=0.5)


def model_variables(run_mode: str, sims_run: int, sim_months: int):
    """
    Loops through the number of simulations run
    Passes the resulting df to make_average_graphs()
    shows the plot at the end
    :param run_mode:
    :param sims_run:
    :param sim_months:
    """
    plt.figure(figsize=(12, 8))
    plt.tick_params(labelsize=8)
    plt.grid()

    for i in range(0, sims_run):
        df = infestation_main(run_mode, sim_months)
        make_average_graphs(df,
                            sim_months)  # hopefully putting this inside the loop will allow the code to forget the df

    plt.show()


"""
Functions used in our visualizations of the simulation
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
from multiprocessing import Pool
from run_simulation import infestation_main


def make_visual_df(simulation_df: pd.DataFrame) -> pd.DataFrame:
    """
    Utility function.
    rotates the run_simulation output df to help with some visualizations
    :param simulation_df:
    :return visual_df:
    """
    visual_df = simulation_df.T
    visual_df.columns = visual_df.iloc[0]
    visual_df = visual_df.drop(visual_df.index[0])
    return visual_df


def make_network_heat(CG, simulation_df, handler, month: int):
    """
    Makes a heatmap from the NX nodes, edges, and object instances
    :param CG:
    :param handler:
    :param simulation_df:
    :param month: The number of months from the interactive ipywidget
    """
    month = f'month {month}'
    #     min_value = simulation_df[month].min()
    #     max_value = simulation_df[month].max()  # This makes the scale variable for each chart
    max_value = 1  # This keeps the scale constant
    min_value = 0
    cmap = matplotlib.colormaps['YlOrRd']

    node_colors = {}
    for node in CG.nodes():
        value = simulation_df.loc[simulation_df['County'] == node.name, month].iloc[0]
        normalized_value = (value - min_value) / (max_value - min_value)
        node_colors[node.name] = cmap(normalized_value)

    labels = {node: handler[node.name].name for node in CG.nodes()}
    fig, ax = plt.subplots(figsize=(10, 15))
    node_positions = {node: [node.centroid.x, node.centroid.y] for node in CG.nodes()}
    nx.draw(CG,
            pos=node_positions,
            ax=ax,
            node_color=[node_colors.get(node.name, 'gray') for node in CG.nodes()],
            node_size=1500, )

    nx.draw_networkx_labels(CG,
                            pos=node_positions,
                            labels=labels,
                            font_size=6,
                            ax=ax,
                            font_color='k')

    edge_colors = ['gray' if CG[src][tgt]['rel'] == 'interstate' else 'gray' for src, tgt in CG.edges()]
    edge_widths = [5 if CG[src][tgt]['rel'] == 'interstate' else 1 for src, tgt in CG.edges()]
    nx.draw_networkx_edges(CG, pos=node_positions, edge_color=edge_colors, ax=ax, width=edge_widths)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min_value, vmax=max_value))
    sm.set_array([])
    sub_ax = plt.axes([0.96, 0.55, 0.02, 0.3])
    plt.colorbar(sm, cax=sub_ax)
    plt.show()


def make_average_graphs(df: pd.DataFrame, sim_months: int):
    """
    Takes the average values over the whole state for each given simulation df.
    Plots them all within the same graph
    :param df:
    :param sim_months:
    """
    vis_df = make_visual_df(df)
    avg_df = vis_df.mean(axis=1)
    plt.xticks(ticks=range(0, sim_months + 1),
               labels=range(0, sim_months + 1))
    plt.xlabel('Months')
    plt.ylabel('Infestation Percentage')
    plt.plot(avg_df.index, avg_df, linewidth=0.5)


def model_variables(run_mode: str, sims_run: int, sim_months: int):
    """
    Loops through the number of simulations run
    Passes the resulting df to make_average_graphs()
    shows the plot at the end
    :param run_mode:
    :param sims_run:
    :param sim_months:
    """
    plt.figure(figsize=(12, 8))
    plt.tick_params(labelsize=8)
    plt.grid()

    for i in range(0, sims_run):
        df = infestation_main(run_mode, sim_months)
        make_average_graphs(df,
                            sim_months)  # hopefully putting this inside the loop will allow the code to forget the df

    plt.show()


def model_variables_avg(run_mode: str, sims_run: int, sim_months: int, all_trends: dict) ->dict:
    """
    A modified version of model_variables
    includes an trend line that averages all the simulations graphed
    Average line is made with the all_trends dict to get passed to the next block of simulations
    :param run_mode:
    :param sims_run:
    :param sim_months:
    :param all_trends:
    :return all_trends:
    """
    plt.figure(figsize=(12, 8))
    plt.title(f'{run_mode} Infestation Model')
    plt.tick_params(labelsize=8)
    all_avg_lines = []

    for i in range(sims_run):
        df = infestation_main(run_mode, sim_months)
        make_average_graphs(df, sim_months)

        vis_df = make_visual_df(df)
        avg_df = vis_df.mean(axis=1)
        all_avg_lines.append(avg_df.values)
    plt.grid()
    if all_avg_lines:
        overall_avg = pd.DataFrame(all_avg_lines).mean()
        plt.plot(overall_avg.index, overall_avg, 'k-', linewidth=3)  # Plotting the overall trend line
    all_trends[run_mode] = overall_avg
    plt.xticks(ticks=range(0, sim_months + 1),
               labels=range(0, sim_months + 1))
    plt.xlabel('Months')
    plt.ylabel('Infestation Percentage')
    plt.show()
    return all_trends

