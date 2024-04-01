# -*- coding: utf-8 -*-
# @Author  : Raphael Maccari
# @Email   : raphaelmaccari@gmail.com
# @File    : ViewVTCDstudy.py
# @Software: PyCharm

from py_dss_tools.view.VTCDSagCircuit import VTCDSagCircuit
from py_dss_tools.view.VTCDSagSwellCircuit import VTCDSagSwellCircuit
from py_dss_tools.view.VTCDVulnerabilityCircuit import VTCDVulnerabilityCircuit
from py_dss_interface import DSS
from py_dss_tools.results.VTCDresults import VTCDresults



class ViewVTCDresults(VTCDSagCircuit, VTCDSagSwellCircuit, VTCDVulnerabilityCircuit):

    def __init__(self, dss: DSS, results: VTCDresults):
        VTCDSagCircuit.__init__(self, dss, results)
        VTCDSagSwellCircuit.__init__(self, dss, results)
        VTCDVulnerabilityCircuit.__init__(self, dss, results)
