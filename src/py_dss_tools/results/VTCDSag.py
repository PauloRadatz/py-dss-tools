# -*- coding: utf-8 -*-
# @Author  : Raphael Maccari
# @Email   : raphaelmaccari@gmail.com
# @File    : VTCDSag.py
# @Software: PyCharm


import pandas as pd
from py_dss_interface import DSS
from py_dss_tools.dss_tools import DSSTools


class VTCDSag:

    def __init__(self, dss: DSS):
        self._dss = dss
        self.vmags_df = pd.DataFrame()

    def sag_3phsc_df_pu(self, bus_fault,v_1=0.1,v_2=0.2,v_3=0.3,v_4=0.4,v_5=0.5,v_6=0.6,v_7=0.7,v_8=0.8,v_9=0.9,v_10=0.95) -> pd.DataFrame:
        self._bus_fault = bus_fault
        self._v_1 = v_1
        self._v_2 = v_2
        self._v_3 = v_3
        self._v_4 = v_4
        self._v_5 = v_5
        self._v_6 = v_6
        self._v_7 = v_7
        self._v_8 = v_8
        self._v_9 = v_9
        self._v_10 = v_10
        self._dss.text(f"new fault.3_ph_{self._bus_fault} phases=3 bus1={self._bus_fault} bus2={self._bus_fault}.4.4.4")
        self._dss.text("solve")
        vmags_df, vangs_df = DSSTools(self._dss).results.circuit_vmag_vang_dfs()
        vmags_df = vmags_df.iloc[:, :-1] #Descarta a última coluna.
        vmags_df['vmin'] = vmags_df.min(axis=1)

        colors = []
        for v_min in vmags_df['vmin']:
            if v_min <= v_1:
                colors.append("black")
            elif v_min <= v_2:
                colors.append("maroon")
            elif v_min <= v_3:
                colors.append("purple")
            elif v_min <= v_4:
                colors.append("navy")
            elif v_min <= v_5:
                colors.append("teal")
            elif v_min <= v_6:
                colors.append("blue")
            elif v_min <= v_7:
                colors.append("aqua")
            elif v_min <= v_8:
                colors.append("yellow")
            elif v_min <= v_9:
                colors.append("lime")
            elif v_min < v_10:
                colors.append("olive")
            else:
                colors.append("green")

        vmags_df['colors'] = colors

        self.vmags_df = vmags_df

        return vmags_df



        # sag_3phsc_df_pu(self, bus_fault, v_1=0.1, v_2=0.5, v_3=0.95)

        # colors = []
        # for v_min in vmags_df['vmin']:
        #     if v_min < v_1:
        #         colors.append("black")
        #     elif v_min < v_2:
        #         colors.append("red")
        #     elif v_min < v_3:
        #         colors.append("yellow")
        #     else:
        #         colors.append("green")
