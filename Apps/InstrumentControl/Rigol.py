from abc import abstractmethod, ABC
import pyvisa
import time


class PURigol(object):
    def __init__(self, visa_manager: pyvisa.ResourceManager, addr: str = 'TCPIP0::192.168.1.227::inst0::INSTR'):
        self.myPU = visa_manager.open_resource(addr)
        print(self.myPU.query("*IDN?"))

    def default_setup_ch1(self):
        """
        Set up overvoltage and overcurrent protection for the first channel of the PU Rigol
        :rtype: object
        """
        self.myPU.write(":OUTP:OCP:VAL CH1,0.1")
        self.myPU.write(":OUTP:OVP:VAL CH1,30")
        self.myPU.write(":OUTP CH1, ON")
        time.sleep(1)
        self.myPU.write(":APPL CH1,0.01,0.01")

    def default_setup_ch2(self):
        """
        Set up overvoltage and overcurrent protection for the second channel of the PU Rigol
        """
        self.myPU.write(":OUTP:OCP:VAL CH2,0.1")
        self.myPU.write(":OUTP:OVP:VAL CH2,30")
        self.myPU.write(":OUTP CH2,ON")
        time.sleep(1)
        self.myPU.write(":APPL CH2,0.01,0.01")

    def v_change_1(self, V1: float):
        """
        Changes voltage on the first channel
        :param V1: meaning of the voltage on the first channel
        """
        self.myPU.write(f":APPL CH1,{V1},0.05")
        time.sleep(1)

    def v_change_2(self, V2: float):
        """
        Changes voltage on the second channel
        :param V2: meaning of the voltage on the second channel
        """
        self.myPU.write(f":APPL CH2,{V2},0.05")
        time.sleep(1)

    def end_of_work(self):
        """
        Turns off the PU Rigol
        """
        self.myPU.write(":OUTP CH1, OFF")
        self.myPU.write(":OUTP CH2, OFF")
        self.myPU.write(":OUTP:OCP:CLEAR CH1")
        self.myPU.write(":OUTP:OCP:CLEAR CH2")

    def reset(self):
        self.myPU.write("*RST")
