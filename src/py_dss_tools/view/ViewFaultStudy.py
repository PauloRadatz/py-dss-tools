# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewFaultResults.py
# @Software: PyCharm


from py_dss_tools.results.ShortCircuit.FaultResults import FaultResults
from py_dss_tools.view.ShortCircuitImpedances import ShortCircuitImpedances
from py_dss_interface import DSS


class ViewFaultResults(ShortCircuitImpedances):

    def __init__(self, dss: DSS, results: FaultResults):
        ShortCircuitImpedances.__init__(self, dss, results)

