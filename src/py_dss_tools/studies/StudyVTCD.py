# -*- coding: utf-8 -*-
# @Author  : Raphael Maccari
# @Email   : raphaelmaccari@gmail.com
# @File    : StudyVTCD.py
# @Software: PyCharm

from py_dss_tools.studies.StudyBase import StudyBase
from py_dss_tools.results.VTCDresults import VTCDresults
from py_dss_tools.view.ViewVTCDstudy import ViewVTCDresults
from dataclasses import dataclass

@dataclass(kw_only=True)
class StudyVTCD(StudyBase):

    def __post_init__(self):
        super().__post_init__()
        self._results = VTCDresults(self._dss) # Object created by composition
        self._view = ViewVTCDresults(self._dss, self._results) # não sei o motivo, mas é necessário haver o self._results
    #     self._view = ViewFaultResults(self._dss, self._results)
    #     self._settings = StudyTemporalSettings(_dss=self.dss)
    @property
    def results(self):
        return self._results

    @property
    def view(self):
        return self._view

#run area vulnerabilit
#run outra coisa??????

#incluir um run aqui, recebe bus name aqui.
