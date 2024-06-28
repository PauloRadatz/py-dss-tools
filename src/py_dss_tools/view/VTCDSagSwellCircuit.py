# -*- coding: utf-8 -*-
# @Author  : Raphael Maccari
# @Email   : raphaelmaccari@gmail.com
# @File    : VTCDSagSwellCircuit.py
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

        bus_fault = self._results._bus_fault
        self._dss.text(f"AddBusMarker Bus={bus_fault} code=7 color=red size=14")

        if vmags_df_circuit.empty:
            raise ValueError("vmags_df is empty. Run sag_swell_1phsc_df_pu method first.")

        for index, row in vmags_df_circuit.iterrows():
            bus_name = index  #Obtém o valor da primeira coluna (bus_name)
            color = row['colors_sag']  #Obtém o valor da coluna "colors_sag"
            self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=7")
        self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000 1ph=3" )

        time.sleep(1)

        self._dss.text(f"ClearBusMarkers") # Fiz isso não repetir as cores

        bus_fault = self._results._bus_fault  # Adicionei
        self._dss.text(f"AddBusMarker Bus={bus_fault} code=7 color=red size=14")

        for index, row in vmags_df_circuit.iterrows():
            bus_name = index  #Obtém o valor da primeira coluna (bus_name)
            color = row['colors_swell']  #Obtém o valor da coluna "colors_swell"
            self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=7")
        self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000 1ph=3")
