# -*- coding: utf-8 -*-
# @Author  : Raphael Maccair
# @Email   : raphaelmaccari@gmail.com
# @File    : VTCDresults.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.dss_tools import DSSTools
import time
import pathlib



class VTCDresults:

    def __init__(self, dss: DSS):
        self._dss = dss

    def sag_3phsc_df_pu(self, bus_fault):
        self._bus_fault = bus_fault
        self._dss.text(f"new fault.3_ph_{self._bus_fault} phases=3 bus1={self._bus_fault} bus2={self._bus_fault}.4.4.4")
        self._dss.text("solve")
        vmags_df, vangs_df = DSSTools(self._dss).results.circuit_vmag_vang_dfs()
        vmags_df['vmin'] = vmags_df.iloc[:, :-1].min(axis=1)
        vmags_df['vmax'] = vmags_df.iloc[:, :-1].max(axis=1)
        print(vmags_df)


        return vmags_df, vangs_df

        # estou trabalhando nesse código aqui para facilitar o acesso via o study example, mas no fim passarei ele para VtcdSagSwell.














        # num_nodes = self._dss.bus.num_nodes #para barra com vários nós.
        # nodes = self._dss.bus.nodes
        # vmags = self._dss.bus.vmag_angle_pu[: 2 * num_nodes: 2]
        # vangs = self._dss.bus.vmag_angle_pu[1: 2 * num_nodes: 2]
        # return round(min(self._dss.bus.vmag_angle_pu[0:6:2]), 2)

    #disponibilizar aqui o


    #Criar uma função nova aqui que aplica o curto em uma barra escolhida e chama a função que o Paulo criou no
    #ResultsUtila que é a circuit_vmag_vang_dfs, assim terei um data frame com as tensões em todas as barras.



