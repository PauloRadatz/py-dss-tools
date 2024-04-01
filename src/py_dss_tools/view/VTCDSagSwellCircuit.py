# -*- coding: utf-8 -*-
# @Author  : Raphael Maccari
# @Email   : raphaelmaccari@gmail.com
# @File    : VTCDSagCircuit.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.results import VTCDresults
import time


class VTCDSagSwellCircuit:

    def __init__(self, dss: DSS, results: VTCDresults):
        self._results = results
        self._dss = dss
        self.vmags_df = None


    def vtcd_sag_swell_circuit(self):

        if self._results is None:
            raise ValueError("VTCDresults object not set. Call set_results method first.")

        vmags_df_circuit = self._results.vmags_df

        if vmags_df_circuit.empty:
            raise ValueError("vmags_df is empty. Run sag_swell_1phsc_df_pu method first.")

        for index, row in vmags_df_circuit.iterrows():
            bus_name = index  # Obtém o valor da primeira coluna (bus_name)
            color = row['colors_sag']  # Obtém o valor da coluna "colors_sag"
            self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=10")
        self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000")

        time.sleep(1)

        self._dss.text(f"ClearBusMarkers") # Fiz isso não repetir as cores

        for index, row in vmags_df_circuit.iterrows():
            bus_name = index  # Obtém o valor da primeira coluna (bus_name)
            color = row['colors_swell']  # Obtém o valor da coluna "colors_swell"
            self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=10")
        self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000")
