import pyvisa
import time
from numpy import arange

V_start, V_max, V_min = 0, 30, -30
step = 0.5
V_plus = arange(V_start, V_max, step)  #Array of positive voltages
V_minus = arange(V_min, V_start, step)  #Array of negative voltages
waveform = [] #Signal from the oscilloscope
time_dom = [] #x axes
amplitude = [] #y axes
max_amp = [] #Meanings of the amplitudes of the pulses

class PURigol (object):
    if __name__ == '__main__':
        rm = pyvisa.ResourceManager()
        myPU = rm.open_resource("TCPIP0::192.168.1.227::inst0::INSTR")
    print (myPU.query("*IDN?"))

    def Deafult_Setup_CH1(self):
        PURigol.myPU.write(":OUTP:OCP:VAL CH1,0.1")
        PURigol.myPU.write (":OUTP:OVP:VAL CH1,30")
        PURigol.myPU.write(":OUTP CH1, ON")
        time.sleep(1)
        PURigol.myPU.write(":APPL CH1,0.01,0.01")
    def Deafult_Setup_CH2(self):
        PURigol.myPU.write(":OUTP:OCP:VAL CH2,0.1")
        PURigol.myPU.write (":OUTP:OVP:VAL CH2,30")
        PURigol.myPU.write(":OUTP CH2,ON")
        time.sleep(1)
        PURigol.myPU.write(":APPL CH2,0.01,0.01")


    # def VoltagesChange (self):
    #     i, j = 0, 0
    #     for i in V_plus:
    #         for j in V_minus:
    #             PURigol.myPU.write ("APPL CH2, j")
    #             j+=step
    #         j=0
    #         i+=step
    #         PURigol.myPU.write("APPL CH1, i")

Rigol = PURigol()
Rigol.Deafult_Setup1()
time.sleep(1)
Rigol.Deafult_Setup2()
#Rigol.VoltagesChange()

