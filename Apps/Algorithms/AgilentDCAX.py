import matplotlib.pyplot as plt
import pyvisa
import numpy as np

ampl = []
i = 0

class OscilloscopeAgilent86100D(object):
    def __init__(self,
                 visa_manager: pyvisa.ResourceManager,
                 addr: str = 'TCPIP0::192.168.1.5::inst0::INSTR'):
        self.myOsc = visa_manager.open_resource(addr)
        print(self.myOsc.query("*IDN?"))

    def Preamble(self):
        return self.myOsc.query(":WAV:PRE?")

    def dataExtraction(self) -> str:
        return self.myOsc.query(":WAVeform:DATA?")

    def GetYData(self, tr_num: int = 1) -> list[float]: # Form array of amplitudes
        data_string = self.dataExtraction()
        data_list = data_string.split(sep=',')
        return [float(x) for x in data_list]

    def GetXdata(self, tr_num: int = 1) -> list[float]: # Form array of time
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

    def width(self):
        width = self.myOsc.query("MEASURE:NWIDTH?")  # The width of the pulse, positive
        return width

    def reset(self):
        self.myOsc.write("*RST")

    def get_osc(self): # Method for getting waveform from the oscilloscope on the screen
        plt.plot(self.GetYData(), self.GetXdata())
        plt.grid(True)
        plt.grid(b=True, which='minor')
        plt.xlabel('Time, sec')
        plt.ylabel('Amplitude, V')
        plt.title('Waveform')
        plt.show()


    def def_setup(self):
        # self.myOsc.write("*RST")
        self.myOsc.write(":TIMEBASE:RANGE 35E-9")  # Time range full scale 10ns
        self.myOsc.write(":CHANNEL1:RANGE 80")  # Voltage range full scale 10
        self.myOsc.write(":WAVEFORM:SOURCE CHANNEL1")
        self.myOsc.write(":SYSTEM:HEADER OFF")
        self.myOsc.write(":CHANNEL1:OFFSET 0")
        self.myOsc.write(":WAVEFORM:FORMAT ASCII")
        self.myOsc.write(":CHANNEL1:PROBE 46 dB")  # Channel 1 attenuation 46 dB
        self.myOsc.write(":TIMEBASE:DELAY 30E-9")
        self.myOsc.write(":TIMEBASE:REFERENCE CENTER ")

    def timebase_change(self, timemax_coord):
        self.myOsc.write(":TIMEBASE:RANGE 2E-9")  # Time range full scale 10ns
        self.myOsc.write(f":TIMEBASE:DELAY {timemax_coord + 0.5E-9}")

if __name__ == '__main__':
    rm = pyvisa.ResourceManager()
    Agil = OscilloscopeAgilent86100D(rm, 'TCPIP0::192.168.1.5::inst0::INSTR')
    Agil.def_setup()

    # plt.plot(time, waveform)
    # plt.grid(True)
    # plt.grid(b = True, which='minor')
    # plt.xlabel('Time, sec')
    # plt.ylabel('Amplitude, V')
    # plt.title('Waveform')
    # plt.show()


