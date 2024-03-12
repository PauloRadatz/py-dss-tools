# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : SummaryModelData.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from py_dss_tools.dss_tools import DSSTools


class SummaryModelData:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def summary_df(self):
        return self.__create_dataframe()

    def __create_dataframe(self):
        return DSSTools(self._dss).model.summary_data()

