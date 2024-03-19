# -*- coding: utf-8 -*-
# @Author  : Raphael Maccari
# @Email   : raphaelmaccari@gmail.com
# @File    : vtcd_study_exemple.py
# @Software: PyCharm


import os
import pathlib
import py_dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "123Bus", "IEEE123Master.dss")

study = py_dss_tools.CreateStudy.vtcd_study(name="VTCD Case 1", dss_file=str(dss_file))
study.dss.text("New EnergyMeter.Feeder Line.L115 1")
study.dss.text(f"Buscoords Buscoords.dat")
study.dss.text("batchedit regcontrol..* enabled=No")
study.dss.text("batchedit load..* enabled=No")

study.results.sag_3phsc_df_pu("95") #ver com o Paulo sobre as barras mono, pois curto 3ph em barra mono não está funcionando
study.view.vtcd_sag_circuit()
print("here")
