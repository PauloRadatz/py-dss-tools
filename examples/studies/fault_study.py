# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : fault_study.py
# @Software: PyCharm

import os
import pathlib

from py_dss_tools import CreateStudy

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("..", "feeders", "123Bus", "IEEE123Master.dss")
bus_coords = pathlib.Path(script_path).joinpath("..", "feeders", "123Bus", "buscoords.dat")

# Creat Static study object
study = CreateStudy.fault_study("My Study", dss_file=dss_file)

# Run faultstudy simulation
study.run(disable_der=True, disable_load=True, disable_capacitor=True)

short_circuit_impedances_df = study.results.short_circuit_impedances

