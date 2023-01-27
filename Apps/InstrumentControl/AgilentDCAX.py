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
        """
    Extracts preamble string from the oscilloscope.
    This string contains data for creation of the array of time
        :return: parsed preamble string
        """
        return self.myOsc.query(":WAV:PRE?")

    def data_extraction(self) -> str:
        """
    Extracts amplitude samples from the oscilloscope. Not parsed
        :return: amplitude samples
        """
        return self.myOsc.query(":WAVeform:DATA?")

    def get_y_data(self) -> list[float]: # Form array of amplitudes
        """
    Parse and form array of amplitude samples from dara, extracted by dataExtraction
        :return: np.array with amplitude samples
        """
        data_string = self.data_extraction()
        data_list = data_string.split(sep=',')
        return [float(x) for x in data_list]

    def get_x_data(self) -> list[float]: # Form array of time
        """
    Forms array of time samples with data, axtracted by @Preamble
        :return: np.arrau with time samples
        """
        preabmle = self.Preamble()
        preabmle = preabmle.split(sep=',')
        points = int(preabmle[2])

        start_time = float(preabmle[12])
        time_range = float(preabmle[11])
        time_end = start_time + time_range

        return list(np.linspace(start_time, time_end, points))

    def amp_width(self):
        """
    Calculation of amplitude and width of the pulse by the oscilloscope`s methods
        :return: float amplitude and float width
        """
        Ampl = self.myOsc.query(":MEASURE:VPP?")  # The amplitude of the pulse, positive
        Width = self.myOsc.query("MEASURE:PWIDTH?")  # The width of the pulse, positive
        return Ampl, Width

    def reset(self):
        """
    Reset of the oscilloscope
        """
        self.myOsc.write("*RST")

    def get_osc(self):
        """
    Plots the waveform from the oscilloscope and shows it on the screen
        """
        plt.plot(self.get_y_data(), self.get_x_data())
        plt.grid(True)
        plt.grid(b=True, which='minor')
        plt.xlabel('Time, sec')
        plt.ylabel('Amplitude, V')
        plt.title('Waveform')
        plt.show()

    def def_setup(self):
        """
    Set default parameters of tre oscilloscope: the time range, channel source, delay and etc
        """
        # self.myOsc.write("*RST")
        self.myOsc.write(":TIMEBASE:RANGE 80E-9")  # Time range full scale 10ns
        self.myOsc.write(":CHANNEL1:RANGE 80")  # V0oltage range full scale 10
        self.myOsc.write(":WAVEFORM:SOURCE CHANNEL1")
        self.myOsc.write(":SYSTEM:HEADER OFF")
        self.myOsc.write(":CHANNEL1:OFFSET 15")
        self.myOsc.write(":WAVEFORM:FORMAT ASCII")
        self.myOsc.write(":CHANNEL1:PROBE 46 dB")  # Channel 1 attenuation 46 dB
        self.myOsc.write(":TIMEBASE:DELAY 15E-9")
        self.myOsc.write(":TIMEBASE:REFERENCE CENTER ")

    def timebase_change(self, timemax_coord: float):
        """
    Dynamic change of the time delay
        :type timemax_coord: float
        :param timemax_coord: time of the max value of the pulse
        """
        self.myOsc.write(":TIMEBASE:RANGE 2E-9")  # Time range full scale 10ns
        self.myOsc.write(f":TIMEBASE:DELAY {timemax_coord + 11E-9}")

    def timebase_change_short(self, timemax_coord: float):
        """
    Dynamic change of the time delay
        :type timemax_coord: float
        :param timemax_coord: time of the max value of the pulse
        """
        self.myOsc.write(":TIMEBASE:RANGE 5E-9")  # Time range full scale 10ns
        self.myOsc.write(f":TIMEBASE:DELAY {timemax_coord + 0.5E-9}")

