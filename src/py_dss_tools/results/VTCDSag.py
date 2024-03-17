


import pandas as pd
from py_dss_interface import DSS
from py_dss_tools.dss_tools import DSSTools


class VTCDSag:

    def __init__(self, dss: DSS):
        self._dss = dss

    def sag_3phsc_df_pu(self, bus_fault,v_1=0.1, v_2=0.5, v_3=0.95) -> pd.DataFrame:
        self._bus_fault = bus_fault
        self._v_1 = v_1
        self._v_2 = v_2
        self._v_3 = v_3
        self._dss.text(f"new fault.3_ph_{self._bus_fault} phases=3 bus1={self._bus_fault} bus2={self._bus_fault}.4.4.4")
        self._dss.text("solve")
        vmags_df, vangs_df = DSSTools(self._dss).results.circuit_vmag_vang_dfs()
        vmags_df = vmags_df.iloc[:, :-1] #Descarta a última coluna.
        vmags_df['vmin'] = vmags_df.min(axis=1)

        colors = []
        for v_min in vmags_df['vmin']:
            if v_min < v_1:
                colors.append("black")
            elif v_min < v_2:
                colors.append("red")
            elif v_min < v_3:
                colors.append("yellow")
            else:
                colors.append("green")

        vmags_df['colors'] = colors

        # Necessito que o codigo abaixo que utiliza o vmags_df acima seja executado em outro arquivo dentro de uma classe.
        # for index, row in vmags_df.iterrows():
        #     bus_name = index  # Obtém o valor da primeira coluna (bus_name)
        #     color = row.iloc[-1]  # Obtém o valor da última coluna (color)
        #     self._dss.text(f"AddBusMarker Bus={bus_name} code=7 color={color} size=10")
        # self._dss.text("plot circuit Power max=2000 n y C1=$00FF0000")
        ###################################

        return vmags_df
