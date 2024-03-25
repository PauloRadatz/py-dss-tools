# -*- coding: utf-8 -*-
# @Author  : Raphael Maccair
# @Email   : raphaelmaccari@gmail.com
# @File    : VTCDresults.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.results.VTCDSag import VTCDSag
from py_dss_tools.results.VTCDSagSwell import VTCDSagSwell
from py_dss_tools.results.VTCDVulnerabilityArea import VTCDVunerabilityArea


class VTCDresults(VTCDSag, VTCDSagSwell,VTCDVunerabilityArea):

    def __init__(self, dss: DSS):
        self._dss = dss
        VTCDSag.__init__(self, self._dss)
        VTCDSagSwell.__init__(self, self._dss)
        VTCDVunerabilityArea.__init__(self, self._dss)
