"""
Functions used in our visualizations of the simulation
TODO: not sure how to write doctests for these
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
    :param simulation_df:
    :return visual_df:
    """
    visual_df = simulation_df.T
    visual_df.columns = visual_df.iloc[0]
    visual_df = visual_df.drop(visual_df.index[0])
    return visual_df


def make_network_heat(CG, simulation_df, handler, iteration: int, time_frame='year'):
    """
    Makes a heatmap from the NX nodes, edges, and object instances
    :param CG: graph of county network
    :param handler: a dictionary with the names of counties for keys and the objects themselves for values
    :param simulation_df:
    :param iteration: The number of iteration from the interactive ipywidget
    """
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

    edge_colors = ['black' if CG[src][tgt]['rel'] == 'interstate' else 'gray' for src, tgt in CG.edges()]
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
    :param sim_iterations: number of iteration in sim runs
    """
    vis_df = make_visual_df(df)
    avg_df = vis_df.mean(axis=1)
    plt.xticks(ticks=range(0, sim_iterations + 1),
               labels=range(0, sim_iterations + 1))
    plt.xlabel('Months')
    plt.ylabel('Infestation Percentage')
    plt.plot(avg_df.index, avg_df, linewidth=0.5)


def model_variables(run_mode: str, sims_run: int, sim_iteration: int, life_cycle=False):
    """
    Loops through the number of simulations run
    Passes the resulting df to make_average_graphs()
    shows the plot at the end
    :param run_mode: The name of the simulation being run
    :param sims_run: number of runs
    :param sim_iteration: number of iteration in each run
    """
    plt.figure(figsize=(12, 8))
    plt.tick_params(labelsize=8)
    plt.grid()

    for i in range(0, sims_run):
        df = saturation_main(run_mode, sim_iteration, life_cycle=life_cycle)
        make_average_graphs(df,
                            sim_iteration)  # hopefully putting this inside the loop will allow the code to forget the df

    plt.show()


def model_variables_avg(run_mode: str, sims_run: int, sim_iteration: int, all_trends: dict, life_cycle=False) -> dict:
    """
    A modified version of model_variables
    includes an trend line that averages all the simulations graphed
    Average line is made with the all_trends dict to get passed to the next block of simulations
    :param run_mode: type of mode the simulation runs in
    :param sims_run: number of runs
    :param sim_iteration: number of iteration per run
    :param all_trends: a dictionary of trends
    :return all_trends:
    """
    plt.figure(figsize=(12, 8))
    plt.title(f'{run_mode} Infestation Model')
    plt.tick_params(labelsize=8)
    all_avg_lines = []

    for i in range(sims_run):
        df = saturation_main(run_mode, sim_iteration, life_cycle=life_cycle)
        make_average_graphs(df, sim_iteration)

        vis_df = make_visual_df(df)
        avg_df = vis_df.mean(axis=1)
        all_avg_lines.append(avg_df.values)
    plt.grid()
    if all_avg_lines:
        overall_avg = pd.DataFrame(all_avg_lines).mean()
        plt.plot(overall_avg.index, overall_avg, 'k-', linewidth=3)  # Plotting the overall trend line
    all_trends[run_mode] = overall_avg
    plt.xticks(ticks=range(0, sim_iteration + 1),
               labels=range(0, sim_iteration + 1))
    plt.xlabel('Months')
    plt.ylabel('Infestation Percentage')
    plt.show()
    return all_trends
