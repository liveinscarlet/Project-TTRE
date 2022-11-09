import numpy as np
import pyvisa
import time
import numpy as np
import numpy.typing as npt

class OscilloscopeAgilent86100D(object):
    def __init__(self,
                 visa_manager: visa.ResourceManager,
                 addr: str = 'TCPIP0::192.168.1.5::inst0::INSTR'):
        myOsc = rm.open_resource(addr)  # Для корректной работы надо отключать защиту осцила
        print(myOsc.query("*IDN?"))

    def dataExtraction(self) -> npt.NDArray[float]:
        return OscilloscopeAgilent86100D.myOsc.query(":WAVeform:DATA?", container=np.array)

    def AmpWidth(self):
        Ampl = OscilloscopeAgilent86100D.myOsc.query(":MEASURE:VPP?")  # The amplitude of the pulse, positive
        Width = OscilloscopeAgilent86100D.myOsc.query("MEASURE:PWIDTH?")  # The width of the pulse, positive
        return Ampl, Width

    def Reset(self):
        OscilloscopeAgilent86100D.myOsc.write("*RST")

    def DefSetup(self):
        OscilloscopeAgilent86100D.myOsc.write("*RST")
        OscilloscopeAgilent86100D.myOsc.write(":TIMEBASE:RANGE 10E-9")  # Time range full scale 10ns
        OscilloscopeAgilent86100D.myOsc.write(":CHANNEL1:RANGE 40")  # Voltage range full scale 10
        OscilloscopeAgilent86100D.myOsc.write(":WAVEFORM:SOURCE CHANNEL1")
        OscilloscopeAgilent86100D.myOsc.write(":WAVEFORM:FORMAT BYTE")
        OscilloscopeAgilent86100D.myOsc.write(":SYSTEM:HEADER OFF")
        OscilloscopeAgilent86100D.myOsc.write(":DIGITIZE CHANNEL1")
        OscilloscopeAgilent86100D.myOsc.write(":CHANNEL1:OFFSET 0")
        OscilloscopeAgilent86100D.myOsc.write(":CHANNEL1:PROBE 46 DEC")  # Channel 1 attenuation 46 dB
