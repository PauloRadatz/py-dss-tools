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

    def sag_3phsc_df_pu(self, bus_fault,v_1=0.1, v_2=0.5, v_3=0.95):
        self._bus_fault = bus_fault
        self._v_1 = v_1
        self._v_2 = v_2
        self._v_3 = v_3
        self._dss.text(f"new fault.3_ph_{self._bus_fault} phases=3 bus1={self._bus_fault} bus2={self._bus_fault}.4.4.4")
        self._dss.text("solve")
        vmags_df, vangs_df = DSSTools(self._dss).results.circuit_vmag_vang_dfs()
        vmags_df = vmags_df.iloc[:, :-1] #Descarta a última coluna.
        vmags_df['vmin'] = vmags_df.min(axis=1)

        colors = []
        for v_min in vmags_df['vmin']:
            if v_min < v_1:
                colors.append("black")
            elif v_min < v_2:
                colors.append("red")
            elif v_min < v_3:
                colors.append("yellow")
            else:
                colors.append("green")

        vmags_df['colors'] = colors

        #o codigo abaixo inserir no VIEW
        for index, row in vmags_df.iterrows():
            bus_name = index  # Obtém o valor da primeira coluna (bus_name)
            color = row.iloc[-1]  # Obtém o valor da última coluna (color)
            self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=10")
        self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000")
        ###################################33

        return vmags_df

        # estou trabalhando nesse código aqui para facilitar o acesso via o study example, mas no fim passarei ele para VtcdSagSwell.














        # num_nodes = self._dss.bus.num_nodes #para barra com vários nós.
        # nodes = self._dss.bus.nodes
        # vmags = self._dss.bus.vmag_angle_pu[: 2 * num_nodes: 2]
        # vangs = self._dss.bus.vmag_angle_pu[1: 2 * num_nodes: 2]
        # return round(min(self._dss.bus.vmag_angle_pu[0:6:2]), 2)

    #disponibilizar aqui o


    #Criar uma função nova aqui que aplica o curto em uma barra escolhida e chama a função que o Paulo criou no
    #ResultsUtila que é a circuit_vmag_vang_dfs, assim terei um data frame com as tensões em todas as barras.



