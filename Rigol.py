from numpy import arange
import numpy as np
import pyvisa
import matplotlib as plt
import time

V_start, V_max, V_min = 0, 30, -30
step = 0.5
V_plus = arange(V_start, V_max, step)  #Array of positive voltages
V_minus = arange(V_min, V_start, step)  #Array of negative voltages
waveform = [] #Signal from the oscilloscope
time_dom = [] #x axes
amplitude = [] #y axes
max_amp = [] #Meanings of the amplitudes of the pulses
low_width = [] #Array of pulses width

class oscil(object):
    if __name__ == '__main__':
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        myOsc = rm.open_resource('TCPIP0::192.168.1.5::inst0::INSTR') #Для корректной работы надо отключать защиту осцила
    print(myOsc.query("*IDN?"))
    def dataExtraction (self):
        oscil.myOsc.query(":WAVeform:DATA?")
        Ampl = oscil.myOsc.query (":MEASURE:VPP?") #The amplitude of the pulse, positive
        Width = oscil.myOsc.query ("MEASURE:PWIDTH?") #The width of the pulse, positive
        return waveform, Ampl, Width

    def DefSetup (self):
        oscil.myOsc.query(":WAVEFORM:SOURCE CHANNEL1")
        oscil.myOsc.query(":WAVEFORM:FORMAT WORD")
        oscil.myOsc.query(":SYSTEM:HEADER OFF")
    pass

class PURigol (object):
    if __name__ == '__main__':
        rm = pyvisa.ResourceManager()
        myPU = rm.open_resource("TCPIP0::192.168.1.227::inst0::INSTR")
    print (myPU.query("*IDN?"))

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

    def Voltage_Change_CH1 (self, V1):
        PURigol.myPU.write(":APPL CH1,V1,0.01")

    def Voltage_Change_CH2 (self, V2):
        PURigol.myPU.write(":APPL CH1,V2,0.01")
    def End_of_Work (self):
        PURigol.myPU.write(":OUTP CH1, OFF")
        PURigol.myPU.write(":OUTP CH2, OFF")
        PURigol.myPU.write (":OUTP:OCP:CLEAR CH1")
        PURigol.myPU.write (":OUTP:OCP:CLEAR CH2")

    pass

# def AmpMeas (waveform): #Программное измерение амплитуды
#     time, amplitude = np.split (waveform, 2)
#
#     return res

#The beginnig of the experiment
#Preexperimental Setup
Rigol = PURigol() #The name of the PU in the experiment
Agilent = oscil() #The name of the osc in the experiment
Rigol.Deafult_Setup_CH1()
time.sleep(1) #Just in case
Rigol.Deafult_Setup_CH2()
Agilent.DefSetup()

#Voltage change
for i in V_plus:
    for j in V_minus:
        Rigol.Voltage_Change_CH2(j)
        Agilent.dataExtraction()
        j += 0.25
    Rigol.Voltage_Change_CH1(i)
    Agilent.dataExtraction()
    Rigol.Voltage_Change_CH2(0)
    i += 0.25

Rigol.End_of_Work()
#The end of the experiment

#Picture of the waveform from the oscilloscope
# plt.plot (t, amplitude)
# plt.grid (True)
# plt.xlabel ('Time, sec')
# plt.ylabel ('Amplitude, V')
# plt.title ('The waveform')

#3D graph for voltages
# fig0 = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(V_plus, V_minus, max_amp, cmap='inferno')

#3D graph for width
# fig0 = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(V_plus, V_minus, low_width, cmap='inferno')
# ax.legend()