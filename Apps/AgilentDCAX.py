import matplotlib.pyplot as plt
import numpy as np
import pyvisa
import time
import numpy as np
import numpy.typing as npt

time = []
ampl = []
i = 0

class OscilloscopeAgilent86100D(object):
    def __init__(self,
                 visa_manager: pyvisa.ResourceManager,
                 addr: str = 'TCPIP0::192.168.1.5::inst0::INSTR'):
        self.myOsc = visa_manager.open_resource(addr)  # Для корректной работы надо отключать защиту осцила
        print(self.myOsc.query("*IDN?"))

    def dataExtraction(self) -> npt.NDArray[float]:
        return self.myOsc.query(":WAVeform:DATA?")

    def AmpWidth(self):
        Ampl = self.myOsc.query(":MEASURE:VPP?")  # The amplitude of the pulse, positive
        Width = self.myOsc.query("MEASURE:PWIDTH?")  # The width of the pulse, positive
        return Ampl, Width

    def Reset(self):
        self.myOsc.write("*RST")

    def DefSetup(self):
        self.myOsc.write("*RST")
        self.myOsc.write(":TIMEBASE:RANGE 10E-9")  # Time range full scale 10ns
        self.myOsc.write(":CHANNEL1:RANGE 40")  # Voltage range full scale 10
        self.myOsc.write(":WAVEFORM:SOURCE CHANNEL1")
        # self.myOsc.write(":WAVEFORM:FORMAT BYTE")
        self.myOsc.write(":SYSTEM:HEADER OFF")
        self.myOsc.write(":CHANNEL1:OFFSET 0")
        # self.myOsc.write(":CHANNEL1:PRlOBE 46 DEC")  # Channel 1 attenuation 46 dB

if __name__ == '__main__':
    rm = pyvisa.ResourceManager()
    Agil = OscilloscopeAgilent86100D(rm, 'TCPIP0::192.168.1.5::inst0::INSTR')
    Agil.DefSetup()
    waveform = Agil.dataExtraction()
    waveform = waveform.split(sep=',')
    # waveform = [float(x) for x in waveform]
    while i < len(waveform):
        if i % 2 == 0:
            time.append(waveform[i])
        else:
            ampl.append(waveform[i])
        i += 1

plt.plot(waveform)
plt.show()
plt.grid(True)
