from abc import abstractmethod, ABC
import pyvisa
import time


class PowerUnit(ABC):
    def __init__(self,
                 visa_manager: pyvisa.ResourceManager,
                 addr: str):
        self.inst = visa_manager.open_resource(addr)
        self._idn = self.idn

    @abstractmethod
    def reset(self):
        # Reset of the Power Unit
        pass

    # @abstractmethod
    # def idn(self) -> str:
    #     # Ask for IDN, check of the connection
    #     idn = self.inst.query('*IDN?')
    #     return idn

    @abstractmethod
    def default_setup_ch1(self):
        # Default setup of the first channel
        pass

    @abstractmethod
    def default_setup_ch2(self):
        # Default setup of the second channel
        pass

    @abstractmethod
    def v_change_1(self, V1):
        # change of the voltage in channel 1
        pass

    @abstractmethod
    def v_change_2(self, V2):
        # change of the voltage in channel 1
        pass

    @abstractmethod
    def end_of_work(self):
        # End of work of the PU
        pass


class PURigol(object):
    def __init__(self, visa_manager: pyvisa.ResourceManager, addr: str = 'TCPIP0::192.168.1.227::inst0::INSTR'):
        # super().__init__(visa_manager, addr)
        self.myPU = visa_manager.open_resource(addr)
        print(self.myPU.query("*IDN?"))

    def default_setup_ch1(self):
        self.myPU.write(":OUTP:OCP:VAL CH1,0.1")
        self.myPU.write(":OUTP:OVP:VAL CH1,30")
        self.myPU.write(":OUTP CH1, ON")
        time.sleep(1)
        self.myPU.write(":APPL CH1,0.01,0.01")

    def default_setup_ch2(self):
        self.myPU.write(":OUTP:OCP:VAL CH2,0.1")
        self.myPU.write(":OUTP:OVP:VAL CH2,30")
        self.myPU.write(":OUTP CH2,ON")
        time.sleep(1)
        self.myPU.write(":APPL CH2,0.01,0.01")

    def v_change_1(self, V1):
        self.myPU.write(f":APPL CH1,{V1},0.05")
        time.sleep(1)

    def v_change_2(self, V2):
        self.myPU.write(f":APPL CH2,{V2},0.05")
        time.sleep(1)

    def end_of_work(self):
        self.myPU.write(":OUTP CH1, OFF")
        self.myPU.write(":OUTP CH2, OFF")
        self.myPU.write(":OUTP:OCP:CLEAR CH1")
        self.myPU.write(":OUTP:OCP:CLEAR CH2")

    def reset(self):
        self.myPU.write("*RST")


class PUGW_Instek(PowerUnit):
    def __init__(self, visa_manager: pyvisa.ResourceManager, addr: str = 'TCPIP0::192.168.1.227::inst0::INSTR'):  # ???????????????? ?? ?????????????????? ???????? ?? ???????????????????? IP
        super().__init__(visa_manager, addr)
        self.myPU = visa_manager.open_resource(addr)
        print(self.myPU.query("*IDN?"))

    def default_setup_ch1(self):
        self.myPU.write(":OUT1")
        self.myPU.write(":SOURCE1:VOLTAGE 0")
        self.myPU.write(":SOURCE1:CURRENT 0.01")

    def default_setup_ch2(self):
        self.myPU.write(":OUT2")
        self.myPU.write(":SOURCE1:VOLTAGE 0")
        self.myPU.write(":SOURCE1:CURRENT 0.01")

    def v_change_1(self, V1):
        self.myPU.write(f":SOURCE1:VOLTAGE {V1}")
        time.sleep(1)

    def v_change_2(self, V2):
        self.myPU.write(f":SOURCE1:VOLTAGE {V2}")
        time.sleep(1)

    def reset(self):
        self.myPU.write("*RST")

    def end_of_work(self):
        self.myPU.write(":ALLOUTOFF")