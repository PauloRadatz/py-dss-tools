# -*- coding: utf-8 -*-
# @Time    : 8/6/2024 5:24 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : vericacao.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "123Bus", "IEEE123Master.dss")

study = py_dss_tools.CreateStudy.model_verification(name="Test", dss_file=str(dss_file))
# study.dss.text("New EnergyMeter.M element=Transformer.Sub terminal=1")
df = study.results.isolated
df1 = study.results.summary
df2 = study.results.loads_transformer_voltage_mismatch
df3 = study.results.same_bus
df4 = study.results.transformer_data
# df4 = study.results.phases_connections

print("here")
