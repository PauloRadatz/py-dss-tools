# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudyFault.py
# @Software: PyCharm

from py_dss_tools.studies.StudyBase import StudyBase
from py_dss_tools.results.FaultResults import FaultResults
from py_dss_tools.view.ViewFaultStudy import ViewFaultResults
from py_dss_tools.studies.StudyFaultSettings import StudyFaultSettings
from dataclasses import dataclass
from py_dss_tools.dss_tools.dss_tools import dss_tools


@dataclass(kw_only=True)
class StudyFault(StudyBase):

    def __post_init__(self):
        super().__post_init__()
        self._results = FaultResults(self._dss)
        self._view = ViewFaultResults(self._dss, self._results)
        self._settings = StudyFaultSettings(_dss=self.dss)

    @property
    def results(self):
        return self._results

    @property
    def view(self):
        return self._view

    @property
    def settings(self):
        return self._settings

    def run(self, disable_der=True, disable_load=True, disable_capacitor=True, control_mode="off"):
        if disable_der:
            dss_tools.model.disable_elements_type("generator")
            dss_tools.model.disable_elements_type("pvsystem")
            dss_tools.model.disable_elements_type("storage")

        if disable_load:
            dss_tools.model.disable_elements_type("load")
            
        if disable_capacitor:
            dss_tools.model.disable_elements_type("capacitor")

        self._dss.text(f"set controlmode={control_mode}")

        self.__check_settings()
        self.dss.text("solve")

    def __check_settings(self):
        self.settings.mode = self.dss.text("get mode")
