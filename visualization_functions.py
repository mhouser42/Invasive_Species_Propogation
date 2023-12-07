"""
Functions used in our visualizations of the simulation
TODO: Once current_month inputs get sorted, then that should fix the doctests.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
from run_simulation import saturation_main


def make_visual_df(simulation_df: pd.DataFrame) -> pd.DataFrame:
    """
    Utility function.
    rotates the run_simulation output df to help with some visualizations
    :param simulation_df: the resulting df from running the MC simulation showing saturation rates
    :return visual_df: a rotated version of simualtion_df with the correct index and columns

    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [0, 0, 0]})
    >>> make_visual_df(df)
    A  1  2  3
    B  0  0  0

    >>> df2 = pd.DataFrame({'A': [1, 2], 'B': [0, 0], 'C': [100, 77]})
    >>> make_visual_df(df2)
    A    1   2
    B    0   0
    C  100  77

    >>> df3 = pd.DataFrame({'E': [13, 45, 15, 0, 0, 0]})
    >>> make_visual_df(df3)
    Empty DataFrame
    Columns: [13, 45, 15, 0, 0, 0]
    Index: []
    """
    visual_df = simulation_df.T
    visual_df.columns = visual_df.iloc[0]
    visual_df = visual_df.drop(visual_df.index[0])
    return visual_df


def make_network_heat(CG: nx.Graph, simulation_df: pd.DataFrame, handler: dict, iteration: int, time_frame=None):
    """
    Makes a heatmap from the NX nodes, edges, and object instances
    :param CG: graph of county network
    :param handler: a dictionary with the names of counties for keys and the objects themselves for values
    :param simulation_df: df generated from on trial instance of the MC simulation
    :param iteration: The number of iterations from the interactive ipywidget
    :param

    >>> simulation_data = {'Cook': ['0', '0', '0'], 'year 1': [0.2, 0.6, 0.8], 'year 2': [0.4, 0.7, 0.5]}
    >>> simulation_df = pd.DataFrame(simulation_data)
    >>> CG = nx.Graph()
    >>> handler = {'A': object(), 'B': object(), 'C': object()}
    >>> make_network_heat(CG, simulation_df, handler, iteration=1)

    # this returns nothing, but passes when given proper input

    """
    time_frame = 'year' if time_frame is None else time_frame

    iteration = f'{time_frame} {iteration}'
    #     min_value = simulation_df[iteration].min()
    #     max_value = simulation_df[iteration].max()  # This makes the scale variable for each chart
    max_value = 1  # This keeps the scale constant
    min_value = 0
    cmap = matplotlib.colormaps['YlOrRd']

    node_colors = {}
    for node in CG.nodes():
        value = simulation_df.loc[simulation_df['County'] == node.name, iteration].iloc[0]
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


def make_average_graphs(df: pd.DataFrame, sim_iterations: int):
    """
    Takes the average values over the whole state for each given simulation df.
    Plots them all within the same graph
    :param df:
    :param sim_iterations: number of iterations in sim runs

    >>> data = {'Year': [0, 1, 2], 'La Salle': [0.2, 0.5, 0.8], 'Williamson': [0.3, 0.6, 0.7]}
    >>> simulation_df = pd.DataFrame(data)
    >>> make_average_graphs(simulation_df, sim_iterations=2)

    # this returns nothing, but passes when given proper input

    >>> data = {'Year': [0, 1, 2], 'La Salle': [0.2, 0.5, 0.8], 'Williamson': [0.3, 0.6, 0.7]}
    >>> simulation_df = pd.DataFrame(data)
    >>> make_average_graphs(simulation_df, sim_iterations=1.5)
    Traceback (most recent call last):
    ...
    TypeError: 'float' object cannot be interpreted as an integer

    >>> data = {'Year': [0, 1, 2], 'La Salle': [0.2, 0.5, 0.8], 'Williamson': [0.3, 0.6, 0.7]}
    >>> make_average_graphs(data, sim_iterations=1)
    Traceback (most recent call last):
    ...
    AttributeError: 'dict' object has no attribute 'T'
    """
    vis_df = make_visual_df(df)
    avg_df = vis_df.mean(axis=1)
    plt.xticks(ticks=range(0, sim_iterations + 1),
               labels=range(0, sim_iterations + 1))
    plt.xlabel('Years')
    plt.ylabel('Saturation Percentage')
    plt.plot(avg_df.index, avg_df, linewidth=0.5)


def model_variables(run_mode: str, sims_run: int, sim_iterations: int, life_cycle=False, prefix=None):
    """
    Loops through the number of simulations run
    Passes the resulting df to make_average_graphs()
    shows the plot at the end
    :param run_mode: The name of the simulation being run
    :param sims_run: number of runs
    :param sim_iterations: number of iterations in each run
    :param life_cycle: Toggles whether the model runs on the annual or month simulation.
    :param prefix: parameter allowing for different graphs/handlers to be loaded in.

    >>> model_variables('Baseline', 5, 3)

    # this returns nothing, but passes when given proper input

    >>> model_variables('Poison ToH', 'SLF', 3)
    Traceback (most recent call last):
    ...
    TypeError: 'str' object cannot be interpreted as an integer

    >>> model_variables('Parasitic Wasp', 7, 3)
    Traceback (most recent call last):
    ...
    ValueError: This is not a valid run mode.

    """
    plt.figure(figsize=(12, 8))
    plt.tick_params(labelsize=8)
    plt.grid()

    prefix = '' if prefix is None else prefix

    for i in range(0, sims_run):
        df = saturation_main(run_mode, sim_iterations, life_cycle=life_cycle, prefix=prefix)
        make_average_graphs(df,
                            sim_iterations)  # hopefully putting this inside the loop will allow the code to forget the df

    plt.show()


def model_variables_avg(run_mode: str, sims_run: int, sim_iterations: int, all_trends: dict,
                        life_cycle=False, prefix=None) -> dict:
    """
    A modified version of model_variables
    includes an trend line that averages all the simulations graphed
    Average line is made with the all_trends dict to get passed to the next block of simulations
    :param run_mode: type of mode the simulation runs in
    :param sims_run: number of runs
    :param sim_iterations: number of iterations per run
    :param all_trends: a dictionary that accumulates trends for each of the simulations run in different modes.
    :param life_cycle: a boolean which determine if the annual or monthly simulation runs.
    :param prefix: alter this to change which network and handlers handled by the system

    :return all_trends: output dict that gets passed to the next run mode simulation.

    >>> all_trends = {}
    >>> result = model_variables_avg('Baseline', 5, 3, all_trends)
    >>> isinstance(result, dict)
    True

    >>> all_trends = {}
    >>> result = model_variables_avg('Flamethrower', 5, 3, all_trends)
    Traceback (most recent call last):
    ...
    ValueError: This is not a valid run mode.

    >>> all_trends = {}
    >>> result = model_variables_avg('Poison ToH', 5.5, 3, all_trends)
    Traceback (most recent call last):
    ...
    TypeError: 'float' object cannot be interpreted as an integer
    """
    prefix = '' if prefix is None else prefix

    plt.figure(figsize=(12, 8))
    plt.title(f'{run_mode} Saturation Model')
    plt.tick_params(labelsize=8)
    all_avg_lines = []

    for i in range(sims_run):
        df = saturation_main(run_mode, sim_iterations, life_cycle=life_cycle, prefix=prefix)
        make_average_graphs(df, sim_iterations)

        vis_df = make_visual_df(df)
        avg_df = vis_df.mean(axis=1)
        all_avg_lines.append(avg_df.values)
    plt.grid()
    if all_avg_lines:
        overall_avg = pd.DataFrame(all_avg_lines).mean()
        plt.plot(overall_avg.index, overall_avg, 'k-', linewidth=3)  # Plotting the overall trend line
    all_trends[run_mode] = overall_avg
    plt.xticks(ticks=range(0, sim_iterations + 1),
               labels=range(0, sim_iterations + 1))
    plt.xlabel('Years')
    plt.ylabel('Saturation Percentage')
    plt.show()
    return all_trends
