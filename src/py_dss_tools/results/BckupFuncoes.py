from py_dss_interface import DSS
import time
from py_dss_tools.dss_utils import DSSUtils
import pathlib


class VTCDresults:

    def __init__(self, dss: DSS):
        self._dss = dss

    # Criar uma função nova aqui que aplica o curto em uma barra escolhida e chama a função que o Paulo criou no
    # ResultsUtila que é a circuit_vmag_vang_dfs, assim terei um data frame com as tensões em todas as barras.


    def sag_3phsc_df_pu(self, bus_fault):
        self._bus_fault = bus_fault
        self._dss.text(f"new fault.3_ph_{self._bus_fault} phases=3 bus1={self._bus_fault} bus2={self._bus_fault}.4.4.4")
        self._dss.text("solve")
        vmags_df, vangs_df = DSSUtils(self._dss).get_circuit_vmag_vang_dfs()
        return vmags_df, vangs_df

    def sag3ph_pu(self, bus_fault, bus_sag):
        self._bus_fault = bus_fault
        self._bus_sag = bus_sag
        self._dss.text(f"new fault.3_ph_{self._bus_fault} phases=3 bus1={self._bus_fault} bus2={self._bus_fault}.4.4.4")
        self._dss.text("solve")
        self._dss.circuit.set_active_bus(self._bus_sag)
        # num_nodes = self._dss.bus.num_nodes #para barra com vários nós.
        # nodes = self._dss.bus.nodes
        # vmags = self._dss.bus.vmag_angle_pu[: 2 * num_nodes: 2]
        # vangs = self._dss.bus.vmag_angle_pu[1: 2 * num_nodes: 2]
        return round(min(self._dss.bus.vmag_angle_pu[0:6:2]), 2)

    def sag_swell_1ph_pu(self, bus_fault, bus_sag_swel):
        self._bus_fault = bus_fault
        self._bus_sag_swell = bus_sag_swel
        self._dss.text(f"new fault.1_ph_{self._bus_fault} phases=1 bus1={self._bus_fault}.1 bus2={self._bus_fault}.0")
        self._dss.text("solve")
        self._dss.circuit.set_active_bus(self._bus_sag_swell)
        return round(min(self._dss.bus.vmag_angle_pu[0:6:2]), 2), round(max(self._dss.bus.vmag_angle_pu[0:6:2]), 2)

    def sag_map_3ph_buses_3ph_sc(self, bus_fault, v_1=0.1, v_2=0.5, v_3=0.95):
        self._bus_fault = bus_fault
        self._v_1 = v_1
        self._v_2 = v_2
        self._v_3 = v_3
        self._dss.text(f"new fault.3_pf_{self._bus_fault} phases=3 bus1={self._bus_fault}")
        self._dss.text("solve")

        bus_color_dict = dict()
        for bus in self._dss.circuit.buses_names:
            self._dss.circuit.set_active_bus(bus)
            if len(self._dss.bus.nodes) >= 3 and self._dss.bus.x:  # Resultados somente para barras trifásicas
                v_min = min(self._dss.bus.vmag_angle_pu[0:6:2])

                if v_min < v_1:
                    bus_color_dict[bus] = "black"
                elif v_min < v_2:
                    bus_color_dict[bus] = "red"
                elif v_min < v_3:
                    bus_color_dict[bus] = "yellow"
                else:
                    bus_color_dict[bus] = "green"

        for bus_name, color in bus_color_dict.items():
            self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=10")

        self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000")

    def sag_swell_maps_1ph_buses_3ph_sc(self, bus_fault, vsag_1=0.1, vsag_2=0.5, vsag_3=0.95, vswell_1=1.05,
                                        vswell_2=1.06, vswell_3=1.1):
        self._bus_fault = bus_fault
        self._vsag_1 = vsag_1
        self._vsag_2 = vsag_2
        self._vsag_3 = vsag_3
        self._vswell_1 = vswell_1
        self._vswell_2 = vswell_2
        self._vswell_3 = vswell_3
        self._dss.text(f"new fault.1_ph_{self._bus_fault} phases=1 bus1={self._bus_fault}.1 bus2={self._bus_fault}.0")
        self._dss.text("solve")

        bus_color_dict_sag = dict()
        for bus in self._dss.circuit.buses_names:
            self._dss.circuit.set_active_bus(bus)
            if len(self._dss.bus.nodes) >= 3 and self._dss.bus.x:  # Resultados somente para barras trifásicas
                v_min = min(self._dss.bus.vmag_angle_pu[0:6:2])

                if v_min < vsag_1:
                    bus_color_dict_sag[bus] = "black"
                elif v_min < vsag_2:
                    bus_color_dict_sag[bus] = "red"
                elif v_min < vsag_3:
                    bus_color_dict_sag[bus] = "yellow"
                else:
                    bus_color_dict_sag[bus] = "green"

        for bus_name, color in bus_color_dict_sag.items():
            self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=10")

        self._dss.text("plot circuit Power max=2000 y y C1=$00FF0000")

        # Tempo em segundos para interromper a execução
        tempo_de_parada = 1  # Alterei para a quantidade desejada de segundos
        time.sleep(tempo_de_parada)

        bus_color_dict_swell = dict()
        for bus in self._dss.circuit.buses_names:
            self._dss.circuit.set_active_bus(bus)
            if len(self._dss.bus.nodes) >= 3 and self._dss.bus.x:  # Resultados somente para barras trifásicas
                v_max = max(self._dss.bus.vmag_angle_pu[0:6:2])

                if v_max <= vswell_1:
                    bus_color_dict_swell[bus] = "green"
                elif v_max <= vswell_2:
                    bus_color_dict_swell[bus] = "yellow"
                elif v_max <= vswell_3:
                    bus_color_dict_swell[bus] = "red"
                else:
                    bus_color_dict_swell[bus] = "black"
        for bus_name, color in bus_color_dict_swell.items():
            self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=10")
        self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000")

    # def compile_dss(self, dss_file: str):
    #     self._dss.text("ClearAll")
    #     self._dss.text("Compile " + "[" + dss_file + "]")

    def bus_vulnerability_sag_map_sc3ph(self, dss_file: str, bus_analyzed, v_1=0.1, v_2=0.5, v_3=0.95):
        self._bus_analyzed = bus_analyzed
        self._v_1 = v_1
        self._v_2 = v_2
        self._v_3 = v_3

        bus_names = list()
        for bus in self._dss.circuit.buses_names:
            self._dss.circuit.set_active_bus(bus)
            if len(self._dss.bus.nodes) >= 3 and self._dss.bus.x:
                bus_names.append(bus)

        bus_color_dict = dict()
        for bus in bus_names:
            # self._dss.text("Compile C:/RaphaelMaccari/GitHub/py-dss-tools/examples/feeders/123Bus/IEEE123Master.dss")
            self._dss.text(f"Compile [{dss_file}]")
            # pensar como fazer o compile com o link automático do aquivo.

            self._dss.text("batchedit regcontrol..* enabled=No")
            self._dss.text("batchedit load..* enabled=No")
            self._dss.text(f"Buscoords Buscoords.dat")
            self._dss.text(f"new fault.3_ph phases=3 bus1={bus}")
            self._dss.text("solve")

            self._dss.circuit.set_active_bus(self._bus_analyzed)

            v_min = min(self._dss.bus.vmag_angle_pu[0:6:2])

            if v_min < v_1:
                bus_color_dict[bus] = "black"
            elif v_min < v_2:
                bus_color_dict[bus] = "red"
            elif v_min < v_3:
                bus_color_dict[bus] = "yellow"
            else:
                print(v_min)
                bus_color_dict[bus] = "green"

        for bus_name, color in bus_color_dict.items():
            self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=10")

        self._dss.text("plot circuit Power max=2000 y n C1=$00FF0000")

