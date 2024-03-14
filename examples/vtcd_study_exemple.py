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

# study.results.sag_swell_1ph_pu("95","57")     #Quado executo mais de uma vez ainda fica o elemento de curto anterior, não sei apagar ainda.
# study.results.sag3ph_pu("95, 57")             #Quado executo mais de uma vez ainda fica o elemento de curto anterior, não sei apagar ainda.
# study.results.sag_map_3ph_buses_3ph_sc("95")  #Quado executo mais de uma vez ainda fica o elemento de curto anterior, não sei apagar ainda.

# study.results.sag_swell_maps_1ph_buses_3ph_sc("95")
# study.results.bus_vulnerability_sag_map_sc3ph(str(dss_file),"52") # fiz automático mas gostaria de digitar somente a barra.

study.results.sag_3phsc_df_pu("95")

print("here")
