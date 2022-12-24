from abc import *
import pyvisa


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
        """
    Set overvoltage and overcurrent protection for PU for the first channel
        """
        # Default setup of the first channel
        pass

    @abstractmethod
    def default_setup_ch2(self):
        """
    Set overvoltage and overcurrent protection for PU for the second channel
        """
        # Default setup of the second channel
        pass

    @abstractmethod
    def v_change_1(self, V1: float):
        """
    Changes voltage on the first channel
        :type V1: float
        :param V1: meaning of the voltage
        """
        # change of the voltage in channel 1
        pass

    @abstractmethod
    def v_change_2(self, V2: float):
        """
    Changes voltage on the second channel
        :type V2: float
        :param V2: meaning of the voltage
        """
        # change of the voltage in channel 1
        pass

    @abstractmethod
    def end_of_work(self):
        """
    Turns off the PU
        """
        # End of work of the PU
        pass