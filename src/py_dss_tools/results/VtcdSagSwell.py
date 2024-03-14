from py_dss_interface import DSS
import time
from py_dss_tools.dss_utils import DSSUtils
import pathlib


class VtcdSagSwell:

    def __init__(self, dss: DSS):
        self._dss = dss
def sag_df_3ph_sc(self, bus_fault, v_1=0.1, v_2=0.5, v_3=0.95):
    self._bus_fault = bus_fault
    self._v_1 = v_1
    self._v_2 = v_2
    self._v_3 = v_3
    self._dss.text(f"new fault.3_pf_{self._bus_fault} phases=3 bus1={self._bus_fault}")
    self._dss.text("solve")
#estou trabalhando nesse código no VTCDresults, para facilitar, mas depois passarei tudo pra cá
    vmags_df, vangs_df = DSSUtils(self._dss).results.circuit_vmag_vang_dfs()



    return vmags_df





    # bus_color_dict = dict()
    # for bus in self._dss.circuit.buses_names:
    #     self._dss.circuit.set_active_bus(bus)
    #     if len(self._dss.bus.nodes) >= 3 and self._dss.bus.x:  # Resultados somente para barras trifásicas
    #         v_min = min(self._dss.bus.vmag_angle_pu[0:6:2])
    #
    #         if v_min < v_1:
    #             bus_color_dict[bus] = "black"
    #         elif v_min < v_2:
    #             bus_color_dict[bus] = "red"
    #         elif v_min < v_3:
    #             bus_color_dict[bus] = "yellow"
    #         else:
    #             bus_color_dict[bus] = "green"
    #
    # for bus_name, color in bus_color_dict.items():
    #     self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=10")
    #
    # self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000")


