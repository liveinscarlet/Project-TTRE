from numpy import arange
import numpy as np
import tkinter
import pyvisa
import matplotlib as plt
import time
from AgilentDCAX import OscilloscopeAgilent86100D
from Rigol import PURigol

V_start, V_max, V_min = 0, 30, -30
step = 0.5
V_plus = arange(V_start, V_max, step)  #Array of positive voltages
V_minus = arange(V_min, V_start, step)  #Array of negative voltages
waveform = [] #Signal from the oscilloscope
time_dom = [] #x axes
amplitude = [] #y axes
max_amp = [] #MeaninSSSSSSSgs of the amplitudes of the pulses
low_width = [] #Array of pulses width

def experiment():
# Preexperimental Setup
    rm = pyvisa.ResourceManager()
    Rigol = PURigol(rm, 'TCPIP0::192.168.1.227::inst0::INSTR')  # The name of the PU in the experiment
    Agilent = OscilloscopeAgilent86100D(rm, 'TCPIP0::192.168.1.5::inst0::INSTR')  # The name of the osc in the exp
    Rigol.Deafult_Setup_CH1()
    time.sleep(1)  # Just in case
    Rigol.Deafult_Setup_CH2()
    Agilent.DefSetup()

    # Voltage change
    for i in V_plus:
        for j in V_minus:
            Rigol.Voltage_Change_CH2(j)
            Agilent.dataExtraction()
            j += 0.25
        Rigol.Voltage_Change_CH1(i)
        Agilent.dataExtraction()
        Rigol.Voltage_Change_CH2(0)
        i += 0.25

    #The end of the experiment
    Rigol.End_of_Work()
    Agilent.Reset()