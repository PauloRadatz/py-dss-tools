# -*- coding: utf-8 -*-
# @Author  : Raphael Maccari
# @Email   : raphaelmaccari@gmail.com
# @File    : VTCDSagCircuit.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.results.VTCDresults import VTCDresults
# from py_dss_tools.results.VTCDSag import VTCDSag


class VTCDSagCircuit:

    def __init__(self, dss: DSS, results: VTCDresults):
        self._results = results
        self._dss = dss


    def vtcd_sag_circuit(self):

        vmags_df = VTCDresults(self._dss).sag_3phsc_df_pu() #quero receber o vmags_df aqui, mas só vou executar essa função no main, após a execução da sag_3phsc_df_pu no main
        # o main possui o nome de vtcd_study_exemple.


        for index, row in vmags_df.iterrows():
            bus_name = index  # Obtém o valor da primeira coluna (bus_name)
            color = row.iloc[-1]  # Obtém o valor da última coluna (color)
            self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=10")
        self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000")




        # vmags_df = # aqui que não sei acessar o "vmags_df" que virá após a execução da função "sag_3phsc_df_pu", e obviamente eu irei executar
        # essa "sag_3phsc_df_pu" primeiramente em meu script master. O que eu quero é chamar esse resultado "vmags_df" aqui para fazer
        # o código abaixo.
