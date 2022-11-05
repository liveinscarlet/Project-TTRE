from numpy import arange
import pyvisa
from pyvisa import query
import matplotlib as plt

V_start, V_max, V_min = 0, 30, -30
step = 0.5
V_plus = arange(V_start, V_max, step)  #Array of positive voltages
V_minus = arange(V_min, V_start, step)  #Array of negative voltages
waveform = [] #Signal from the oscilloscope
time_dom = [] #x axes
amplitude = [] #y axes
max_amp = [] #Meanings of the amplitudes of the pulses

class oscil(object):
    if __name__ == '__main__':
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        myOsc = rm.open_resource('TCPIP0::192.168.5::inst0::INSTR') #Для корректной работы надо отключать защиту осцила
    print(myOsc.query("*IDN?"))
    def dataExtraction (self):
        oscil.myOsc.query(":WAVeform:DATA?")

    def DefSetup (self):
        oscil.myOsc.query(":WAVEFORM:SOURCE CHANNEL1")
        oscil.myOsc.query(":WAVEFORM:FORMAT WORD")
        oscil.myOsc.query(":SYSTEM:HEADER OFF")
        return waveform
    pass

class PURigol (object):
    if __name__ == '__main__':
        rm = pyvisa.ResourceManager()
        myPU = rm.open_resource("TCPIP0::192.168.1.227::inst0::INSTR")
    print (myPU.query("*IDN?"))

    def Deafult_Setup(self):
        PURigol.myPU.query(":CH1 :CURR:PROT 0.1")
        PURigol.myPU.query(":CH2 :CURR:PROT 0.1")
        PURigol.myPU.query(":APPL CH1,0,0")
        PURigol.myPU.query(":APPL CH2,0,0")

    def VoltagesChange (self):
        i, j = 0, 0
        for i in V_plus:
            for j in V_minus:
                PURigol.myPU.query ("APPL CH2, j")
                j+=step
            j=0
            i+=step
            PURigol.myPU.query("APPL CH1, i")

    def SetVolt (self, volt_plus, volt_minus):
        PURigol.myPU.query(":APPL CH1, volt_plus")
        PURigol.myPU.query(":APPL CH2, volt_minus")

    pass

def AmpMeas (waveform):
    time, amplitude = np.split (waveform, 2)

    return res

#Picture of the waveform from the oscilloscope
# plt.plot (t, amplitude)
# plt.grid (True)

#3D graph for voltages
fig0 = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='inferno')
ax.legend()