# -*- coding: utf-8 -*-
# @Author  : Raphael Maccari
# @Email   : raphaelmaccari@gmail.com
# @File    : VTCDbusesNameTag.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.results.VTCDresults import VTCDresults


class VTCDbusesNameTag:

    def __init__(self, dss: DSS, results: VTCDresults):
        self._results = results
        self._dss = dss


    def plot_circuit_buses_name(self):
        self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000")



