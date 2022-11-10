from numpy import arange
import numpy as np
import pyvisa
import matplotlib as plt
import time

class PURigol(object):
    def __init__(self,
                 visa_manager: pyvisa.ResourceManager,
                 addr: str = 'TCPIP0::192.168.1.227::inst0::INSTR'):
        myPU = rm.open_resource(addr)
    print(myPU.query("*IDN?"))

    def Deafult_Setup_CH1(self):
        PURigol.myPU.write(":OUTP:OCP:VAL CH1,0.1")
        PURigol.myPU.write(":OUTP:OVP:VAL CH1,30")
        PURigol.myPU.write(":OUTP CH1, ON")
        time.sleep(1)
        PURigol.myPU.write(":APPL CH1,0.01,0.01")

    def Deafult_Setup_CH2(self):
        PURigol.myPU.write(":OUTP:OCP:VAL CH2,0.1")
        PURigol.myPU.write(":OUTP:OVP:VAL CH2,30")
        PURigol.myPU.write(":OUTP CH2,ON")
        time.sleep(1)
        PURigol.myPU.write(":APPL CH2,0.01,0.01")

    def Voltage_Change_CH1(self, V1):
        PURigol.myPU.write(":APPL CH1,V1,0.01")

    def Voltage_Change_CH2(self, V2):
        PURigol.myPU.write(":APPL CH1,V2,0.01")

    def End_of_Work(self):
        PURigol.myPU.write(":OUTP CH1, OFF")
        PURigol.myPU.write(":OUTP CH2, OFF")
        PURigol.myPU.write(":OUTP:OCP:CLEAR CH1")
        PURigol.myPU.write(":OUTP:OCP:CLEAR CH2")
