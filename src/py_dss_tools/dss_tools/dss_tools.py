# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : dss_tools.py
# @Software: PyCharm


from dataclasses import dataclass
from typing import Optional, Union
from py_dss_interface import DSS
import pandas as pd
# from py_dss_tools.dss_tools.ResultsTools import ResultsTools
# from py_dss_tools.dss_tools.ModelTools import ModelTools
from py_dss_tools.dss_tools.DSSViewTools import DSSViewTools
from py_dss_tools.dss_tools.SimulationTools import SimulationTools
from py_dss_tools.dss_tools.ConfigurationTools import ConfigurationTools
from py_dss_tools.dss_tools.UtilitiesTools import UtilitiesTools


class DSSTools:

    def __init__(self, dss: Optional[DSS]):
        self._dss = dss

        if dss:
            self.__load_objects()

    def __load_objects(self):
        # self._results = ResultsTools(self._dss)
        from py_dss_tools.results.Results import Results
        from py_dss_tools.model.ModelBase import ModelBase
        from py_dss_tools.static_view.ViewResults import ViewResults as StaticView
        from py_dss_tools.interactive_view.ViewResults import ViewResults as InteractiveView
        self._results = Results(self._dss)
        self._model = ModelBase(self._dss)
        self._dss_view = DSSViewTools(self._dss)
        self._static_view = StaticView(self._dss, self._results)
        self._interactive_view = InteractiveView(self._dss, self._results)
        self._simulation = SimulationTools(self._dss)
        self._configuration = ConfigurationTools(self._dss)
        self._utilities = UtilitiesTools(self._dss)

    def update_dss(self, dss: DSS):
        self._dss = dss
        self.__load_objects()

    @property
    def results(self):
        return self._results

    @property
    def model(self):
        return self._model

    @property
    def dss_view(self):
        return self._dss_view

    @property
    def static_view(self):
        return self._static_view

    @property
    def interactive_view(self):
        return self._interactive_view

    @property
    def simulation(self):
        return self._simulation

    @property
    def configuration(self):
        return self._configuration

    @property
    def utilities(self):
        return self._utilities

    def text(self, command: str):
        self._dss.text(command)


dss_tools = DSSTools(None)
