from abc import abstractmethod, ABC

from numpy import arange
import numpy as np
import pyvisa
import matplotlib as plt
import time

# @ABC
# class PowerUnit:
#     def __init__(self,
#                  visa_manager: pyvisa.ResourceManager,
#                  addr: str):
#         self.inst = visa_manager.open_resource(addr)
#         self._idn = self.idn
#
#     @abstractmethod
#     def reset(self):
#         # Reset of the Power Unit
#         pass
#
#     @property
#     def idn(self) -> str:
#         # Ask for IDN, check of the connection
#         return self.inst.query('*IDN?')

    # @Voltages
    # def voltages(self):


class PURigol(object):
    def __init__(self,
                 visa_manager: pyvisa.ResourceManager,
                 addr: str = 'TCPIP0::192.168.1.227::inst0::INSTR'):
        self.myPU = visa_manager.open_resource(addr)  # Для корректной работы надо отключать защиту осцила
        print(self.myPU.query("*IDN?"))

    def Deafult_Setup_CH1(self):
        self.myPU.write(":OUTP:OCP:VAL CH1,0.1")
        self.myPU.write(":OUTP:OVP:VAL CH1,30")
        self.myPU.write(":OUTP CH1, ON")
        time.sleep(1)
        self.myPU.write(":APPL CH1,0.01,0.01")

    def Deafult_Setup_CH2(self):
        self.myPU.write(":OUTP:OCP:VAL CH2,0.1")
        self.myPU.write(":OUTP:OVP:VAL CH2,30")
        self.myPU.write(":OUTP CH2,ON")
        time.sleep(1)
        self.myPU.write(":APPL CH2,0.01,0.01")

    def Voltage_Change_CH1(self, V1):
        self.myPU.write(f":APPL CH1,{V1},0.05")
        time.sleep(1)

    def Voltage_Change_CH2(self, V2):
        self.myPU.write(f":APPL CH2,{V2},0.05")
        time.sleep(1)

    def End_of_Work(self):
        self.myPU.write(":OUTP CH1, OFF")
        self.myPU.write(":OUTP CH2, OFF")
        self.myPU.write(":OUTP:OCP:CLEAR CH1")
        self.myPU.write(":OUTP:OCP:CLEAR CH2")


