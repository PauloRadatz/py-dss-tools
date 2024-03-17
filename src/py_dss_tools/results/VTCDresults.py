# -*- coding: utf-8 -*-
# @Author  : Raphael Maccair
# @Email   : raphaelmaccari@gmail.com
# @File    : VTCDresults.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.results.VTCDSag import VTCDSag


class VTCDresults(VTCDSag):

    def __init__(self, dss: DSS):
        self._dss = dss
        VTCDSag.__init__(self, self._dss)
