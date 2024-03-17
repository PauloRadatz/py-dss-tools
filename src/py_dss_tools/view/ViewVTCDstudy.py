# -*- coding: utf-8 -*-
# @Author  : Raphael Maccari
# @Email   : raphaelmaccari@gmail.com
# @File    : ViewVTCDstudy.py
# @Software: PyCharm

from py_dss_tools.view.VTCDSagCircuit import VTCDSagCircuit
from py_dss_interface import DSS
from py_dss_tools.results.VTCDresults import VTCDresults


class ViewVTCDresults(VTCDSagCircuit):

    def __init__(self, dss: DSS, results: VTCDresults):
        VTCDSagCircuit.__init__(self, dss, results)



        # self._dss = dss #estava aqui, mas está tomando conta dentro da classe VTCbusesNameTag
        # self._results = results #estava aqui, mas está tomando conta dentro da classe VTCbusesNameTag


    # def plot_circuit_buses_name_tag(self): # passei essa função para a classe VTCbusesNameTag, pois neste aquivo
                                             # herdarei cada arquivo de funcionalidade que for criado.
    #     self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000")







        # PlotCircuitBusesNameTag.__init__(self, dss, results)


# from py_dss_tools.results.FaultResults import FaultResults
# from py_dss_tools.view.ShortCircuitImpedances import ShortCircuitImpedances
# from py_dss_interface import DSS
#
#
# class ViewFaultResults(ShortCircuitImpedances):
#
#     def __init__(self, dss: DSS, results: FaultResults):
#         ShortCircuitImpedances.__init__(self, dss, results)
