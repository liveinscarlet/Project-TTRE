import matplotlib.pyplot as plt
import numpy as np
import pyvisa
import time
import numpy as np
import numpy.typing as npt

ampl = []
i = 0

class OscilloscopeAgilent86100D(object):
    def __init__(self,
                 visa_manager: pyvisa.ResourceManager,
                 addr: str = 'TCPIP0::192.168.1.5::inst0::INSTR'):
        self.myOsc = visa_manager.open_resource(addr)  # Для корректной работы надо отключать защиту осцила
        print(self.myOsc.query("*IDN?"))

    def Preamble(self):
        return self.myOsc.query(":WAV:PRE?")

    def dataExtraction(self) -> str:
        return self.myOsc.query(":WAVeform:DATA?")

    def GetYData(self, tr_num: int = 1) -> list[float]:
        data_string = self.dataExtraction()
        data_list = data_string.split(sep=',')
        return [float(x) for x in data_list]

    def GetXdata(self, tr_num: int = 1) -> list[float]:
        preabmle = self.Preamble()
        preabmle = preabmle.split(sep=',')
        points = int(preabmle[2])

        start_time = float(preabmle[12])
        time_range = float(preabmle[11])
        time_end = start_time + time_range

        return list(np.linspace(start_time, time_end, points))

    def AmpWidth(self):
        Ampl = self.myOsc.query(":MEASURE:VPP?")  # The amplitude of the pulse, positive
        Width = self.myOsc.query("MEASURE:PWIDTH?")  # The width of the pulse, positive
        return Ampl, Width

    def Reset(self):
        self.myOsc.write("*RST")

    def DefSetup(self):
        # self.myOsc.write("*RST")
        self.myOsc.write(":TIMEBASE:RANGE 10E-9")  # Time range full scale 10ns
        self.myOsc.write(":CHANNEL1:RANGE 40")  # Voltage range full scale 10
        self.myOsc.write(":WAVEFORM:SOURCE CHANNEL1")
        self.myOsc.write(":SYSTEM:HEADER OFF")
        self.myOsc.write(":CHANNEL1:OFFSET 0")
        self.myOsc.write(":WAVEFORM:FORMAT ASCII")
        # self.myOsc.write(":CHANNEL1:PRlOBE 46 DEC")  # Channel 1 attenuation 46 dB

if __name__ == '__main__':
    rm = pyvisa.ResourceManager()
    Agil = Oscilloscope_Agilent86100D(rm, 'TCPIP0::192.168.1.5::inst0::INSTR')
    Agil.DefSetup()
    preabmle = Agil.Preamble()
    preabmle = preabmle.split(sep=',')
    points = int(preabmle[2])

    # The time array formation
    start_time = float(preabmle[12])
    time_range = float(preabmle[11])
    time_end = start_time+time_range
    time = np.linspace(start_time, time_end, points)

    waveform = Agil.dataExtraction()
    waveform = waveform.split(sep=',')
    waveform = [float(x) for x in waveform]

    plt.plot(time, waveform)
    plt.show()
    plt.grid(True)
    plt.ylim(-1, 1)
