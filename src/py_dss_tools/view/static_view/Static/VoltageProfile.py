# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfile.py
# @Software: PyCharm

import matplotlib.pyplot as plt
from py_dss_tools.results.Static.StaticResults import StaticResults
from py_dss_interface import DSS
from py_dss_tools.view.static_view.CustomPlotStyle import CustomPlotStyle
from typing import Optional, Union, Tuple, List
from py_dss_tools.view.static_view.Static.VoltageProfileBusMarker import VoltageProfileBusMarker
from py_dss_tools.view.view_base.VoltageProfileBase import VoltageProfileBase


class VoltageProfile(VoltageProfileBase):

    def __init__(self, dss: DSS, results: StaticResults):
        self._results = results
        self._dss = dss
        VoltageProfileBase.__init__(self, self._dss, self._results)

        self._plot_style = CustomPlotStyle()

    @property
    def voltage_profile_plot_style(self):
        return self._plot_style

    def voltage_profile_get_bus_mark(self, name: str, symbol: str = "x",
                                     size: float = 10,
                                     color: str = "black",
                                     annotate: bool = False,
                                     annotation_label: Optional[str] = None,
                                     annotation_delta_x: float = -0.02,
                                     annotation_delta_y: float = -0.02,
                                     show_legend: bool = False):
        if not annotation_label:
            annotation_label = name
        return VoltageProfileBusMarker(name=name,
                                       symbol=symbol,
                                       size=size,
                                       color=color,
                                       annotate=annotate,
                                       annotation_label=annotation_label,
                                       annotation_delta_x=annotation_delta_x,
                                       annotation_delta_y=annotation_delta_y,
                                       show_legend=show_legend)

    def voltage_profile(self,
                        title: Optional[str] = "Voltage Profile",
                        xlabel: Optional[str] = "Distance",
                        ylabel: Optional[str] = "Voltage (pu)",
                        xlim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        ylim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        buses_marker: Optional[List[VoltageProfileBusMarker]] = None,
                        tight_layout: Optional[bool] = True,
                        legend: Optional[bool] = True,
                        dpi: Optional[int] = 200,
                        save_file_path: Optional[str] = None,
                        show: Optional[bool] = True,
                        **kwargs
                        ):
        self._check_energymeter()

        self._plot_style.apply_style()
        fig, ax = plt.subplots()
        for key, value in kwargs.items():
            setattr(fig, key, value)

        buses, df, distances, sections = self._prepare_results()
        node_colors = {1: 'black', 2: 'red', 3: 'blue'}

        bus_annotated = list()
        legend_handles = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_colors[node], markersize=10)
            for node in range(1, 4)
        ]
        legend_labels = [f'Node {node}' for node in range(1, 4)]

        # Dictionary to track which bus markers have been added to the legend
        legend_added = {}

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
                                marker=bus_marker.symbol,
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

                        # Add the bus marker to the legend if show_legend is True and not already added
                        if bus_marker.show_legend and bus_marker.annotation_label not in legend_added:
                            handle = plt.Line2D([0], [0],
                                                marker=bus_marker.symbol,
                                                color=bus_marker.color,
                                                linestyle='None',
                                                markersize=bus_marker.size,
                                                markerfacecolor=bus_marker.color,
                                                markeredgecolor=bus_marker.color)
                            legend_handles.append(handle)
                            legend_labels.append(bus_marker.annotation_label)
                            legend_added[bus_marker.annotation_label] = True  # Mark this marker as added

        # Create the legend
        if legend:
            ax.legend(legend_handles, legend_labels)

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
