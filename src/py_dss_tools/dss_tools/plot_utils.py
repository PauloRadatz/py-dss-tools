# -*- coding: utf-8 -*-
# @Time    : 3/30/2024 1:07 PM
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : plot_utils.py
# @Software: PyCharm

import pandas as pd
from typing import Dict
import matplotlib.pyplot as plt
from typing import Optional, Union, Tuple, List
from py_dss_tools.view.CustomPlotStyle import CustomPlotStyle
from py_dss_interface import DSS
from py_dss_tools.dss_tools.VoltageProfileBusMarker import VoltageProfileBusMarker


def voltage_profile(dss: DSS,
                    results: pd.DataFrame,
                    plot_style: CustomPlotStyle,
                    title: Optional[str],
                    xlabel: Optional[str],
                    ylabel: Optional[str],
                    xlim: Optional[Tuple[Union[int, float], Union[int, float]]],
                    ylim: Optional[Tuple[Union[int, float], Union[int, float]]],
                    buses_marker: Optional[List[VoltageProfileBusMarker]],
                    tight_layout: Optional[bool],
                    legend: Optional[bool],
                    dpi: Optional[int],
                    save_file_path: Optional[str],
                    show: Optional[bool],
                    **kwargs
                    ):
    if dss.meters.count == 0:
        raise ValueError(f'One enerymeter should exist to plot the voltage profile.')
    elif dss.meters.count > 1:
        count_enabled = 0
        dss.meters.first()
        for _ in range(dss.meters.count):
            dss.circuit.set_active_element(f"energymeter.{dss.meters.name}")
            if dss.cktelement.is_enabled:
                count_enabled += 1
            dss.meters.next()

        if count_enabled == 0:
            raise ValueError(f'At least one enerymeter should be enabled to plot the voltage profile.')
        elif count_enabled > 1:
            raise ValueError(f'Only one enerymeter should be enabled to plot the voltage profile.')

    plot_style.apply_style()
    fig, ax = plt.subplots()
    for key, value in kwargs.items():
        setattr(fig, key, value)

    df = results
    buses = [bus.lower().split(".")[0] for bus in dss.circuit.buses_names]
    distances = dss.circuit.buses_distances

    sections = list()

    elements_list = dss.circuit.elements_names
    for element in elements_list:
        if element.split(".")[0].lower() in ["line", "reactor"]:
            dss.circuit.set_active_element(element)
            if dss.cktelement.is_enabled:
                sections.append(
                    (dss.cktelement.bus_names[0].lower().split(".")[0],
                     dss.cktelement.bus_names[1].lower().split(".")[0]))

    node_colors = {1: 'black', 2: 'red', 3: 'blue'}
    plt.figure(figsize=(10, 6))

    bus_annotated = list()
    for node in range(1, 4):
        for section in sections:
            bus1, bus2 = section
            distance1 = distances[buses.index(bus1)]
            distance2 = distances[buses.index(bus2)]
            ax.plot([distance1, distance2], [df.loc[bus1, f'node{node}'], df.loc[bus2, f'node{node}']], marker='o',
                    color=node_colors[node])

            if buses_marker:
                bus_marker = next((bus for bus in buses_marker if bus.name == bus1), None)
                if bus_marker:
                    ax.plot(distance1, df.loc[bus1, f'node{node}'],
                            marker=bus_marker.marker,
                            markersize=bus_marker.size,
                            color=bus_marker.color)

                    if bus1 not in bus_annotated:
                        if bus_marker.annotate:
                            ax.annotate(bus_marker.annotation_label,
                                        xy=(distance1, df.loc[bus1, f'node{node}']),
                                        xytext=(distance1 + bus_marker.annotation_delta_x,
                                                df.loc[bus1, f'node{node}'] + bus_marker.annotation_delta_y),
                                        arrowprops=dict(facecolor='black', shrink=0.05),
                                        )
                        bus_annotated.append(bus1)

    if legend:
        legend_labels = [f'Node {node}' for node in range(1, 4)]
        legend_handles = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_colors[node], markersize=10)
            for node in range(1, 4)]
        fig.legend(legend_handles, legend_labels)

    fig.suptitle(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    if tight_layout:
        fig.tight_layout()

    fig.set_dpi(dpi)

    if save_file_path:
        fig.savefig(save_file_path, format="png", dpi=300, bbox_inches='tight')

    if show:
        plt.show()


def vmag_vs_time(dss: DSS,
                 df: pd.DataFrame,
                 plot_style: CustomPlotStyle,
                 name: str,
                 unit: str,
                 title: Optional[str],
                 xlabel: Optional[str],
                 ylabel: Optional[str],
                 xlim: Optional[Tuple[Union[int, float], Union[int, float]]],
                 ylim: Optional[Tuple[Union[int, float], Union[int, float]]],
                 tight_layout: Optional[bool],
                 legend: Optional[bool],
                 dpi: Optional[int],
                 save_file_path: Optional[str],
                 show: Optional[bool],
                 **kwargs
                 ):

    if name.lower() not in dss.monitors.names:
        raise ValueError(f"{name} is not a monitor")

    plot_style.apply_style()

    fig, ax = plt.subplots()
    for key, value in kwargs.items():
        setattr(fig, key, value)

    dss.monitors.name = name
    m_mode = dss.monitors.mode
    vi_polar = dss.text(f"? monitor.{name}.vipolar").lower()

    element = dss.monitors.element
    terminal = dss.monitors.terminal

    dss.circuit.set_active_element(element)
    elem_num_phases = dss.cktelement.num_phases
    elem_num_conductors = dss.cktelement.num_conductors
    if terminal == 1:
        elem_nodes = dss.cktelement.node_order[: elem_num_phases]
        bus = dss.cktelement.bus_names[0].split(".")[0]
        dss.circuit.set_active_bus(bus)
        v_base = dss.bus.kv_base * 1000.0
    elif terminal == 2:
        elem_nodes = dss.cktelement.node_order[elem_num_conductors: elem_num_conductors + elem_num_phases]
    else:
        raise ValueError(f'terminal=3 not implemented')

    if m_mode != 0:
        error_message = f'Invalid monitor mode. It should be 0 not {m_mode}'
        raise ValueError(error_message)
    if vi_polar in ["false", "no"]:
        raise ValueError(f'Invalid monitor vipolar. It should be True or Yes not {vi_polar}')

    node_colors = {1: 'black', 2: 'red', 3: 'blue'}

    for index, node in enumerate(elem_nodes):
        if unit == "kV":
            df[f" V{index + 1}"] = df[f" V{index + 1}"] / 1000.0
        elif unit == "pu":
            df[f" V{index + 1}"] = df[f" V{index + 1}"] / v_base
        ax.plot(df["Hour"], df[f" V{index + 1}"], color=node_colors[node], label=f"V{node}")

    fig.suptitle(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    if tight_layout:
        fig.tight_layout()

    if legend:
        ax.legend()

    fig.set_dpi(dpi)

    if save_file_path:
        plt.savefig(save_file_path)

    if show:
        plt.show()


def p_vs_time(dss: DSS,
              df: pd.DataFrame,
              plot_style: CustomPlotStyle,
              name: str,
              unit: str,
              title: Optional[str],
              xlabel: Optional[str],
              ylabel: Optional[str],
              xlim: Optional[Tuple[Union[int, float], Union[int, float]]],
              ylim: Optional[Tuple[Union[int, float], Union[int, float]]],
              tight_layout: Optional[bool],
              legend: Optional[bool],
              dpi: Optional[int],
              save_file_path: Optional[str],
              show: Optional[bool],
              **kwargs
              ):
    if name.lower() not in dss.monitors.names:
        raise ValueError(f"{name} is not a monitor")

    plot_style.apply_style()

    fig, ax = plt.subplots()
    for key, value in kwargs.items():
        setattr(fig, key, value)

    dss.monitors.name = name
    m_mode = dss.monitors.mode
    p_polar = dss.text(f"? monitor.{name}.ppolar").lower()

    element = dss.monitors.element
    terminal = dss.monitors.terminal

    dss.circuit.set_active_element(element)
    elem_num_phases = dss.cktelement.num_phases
    elem_num_conductors = dss.cktelement.num_conductors
    if terminal == 1:
        elem_nodes = dss.cktelement.node_order[: elem_num_phases]
    elif terminal == 2:
        elem_nodes = dss.cktelement.node_order[elem_num_conductors: elem_num_conductors + elem_num_phases]
    else:
        raise ValueError(f'terminal=3 not implemented')

    if m_mode != 1:
        raise ValueError(f'Invalid monitor mode. It should be 1 not {m_mode}')
    if p_polar in ["true", "yes"]:
        raise ValueError(f'Invalid monitor ppolar. It should be True or Yes not {p_polar}')


    node_colors = {1: 'black', 2: 'red', 3: 'blue'}

    for index, node in enumerate(elem_nodes):
        if unit == "kW":
            pass
        ax.plot(df["Hour"], df[f" P{index + 1} (kW)"], color=node_colors[node], label=f"P{node}")

    fig.suptitle(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    if tight_layout:
        fig.tight_layout()

    if legend:
        ax.legend()

    fig.set_dpi(dpi)

    if save_file_path:
        plt.savefig(save_file_path)

    if show:
        plt.show()
