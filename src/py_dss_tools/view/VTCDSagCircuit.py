# -*- coding: utf-8 -*-
# @Author  : Raphael Maccari
# @Email   : raphaelmaccari@gmail.com
# @File    : VTCDSagCircuit.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.results import VTCDresults


class VTCDSagCircuit:

    def __init__(self, dss: DSS, results):
        self._results = results
        self._dss = dss
        self.vmags_df = None


    def vtcd_sag_circuit(self):

        if self._results is None:
            raise ValueError("VTCDresults object not set. Call set_results method first.")

        vmags_df_circuit = self._results.vmags_df

        if vmags_df_circuit.empty:
            raise ValueError("vmags_df is empty. Run sag_3phsc_df_pu method first.")

        bus_fault = self._results._bus_fault
        self._dss.text(f"AddBusMarker Bus={bus_fault} code=7 color=red size=14")  #Destaca a barra

        for index, row in vmags_df_circuit.iterrows():
            bus_name = index  # Obtém o valor da primeira coluna (bus_name)
            color = row.iloc[-1]  # Obtém o valor da última coluna (color)
            self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=7")
        self._dss.text("plot circuit Power max=0 n y C1=$00FF0000 1ph=3")
