from numpy import arange
import numpy as np
import tkinter
import pyvisa
import time
from AgilentDCAX import Oscilloscope_Agilent86100D
from Rigol import PURigol

waveform = []  # Signal from the oscilloscope
time_dom = []  # x axes
amplitude = []  # y axes
max_amp = []  # Meanings of the amplitudes of the pulses
pulse_width = []  # Array of pulses width


class Experiment(object):
    def __init__(self,
                 resource_manager,
                 addr_pu: str = 'TCPIP0::192.168.1.227::inst0::INSTR',
                 addr_osc: str = 'TCPIP0::192.168.1.5::inst0::INSTR'):
        self.rm = resource_manager
        self.pu = PURigol(self.rm, addr_pu)  # The name of the PU in the experiment
        self.ocs = Oscilloscope_Agilent86100D(rm, addr_osc)  # The name of the osc in the exp

        self.pu.Deafult_Setup_CH1()
        self.pu.Deafult_Setup_CH2()
        self.ocs.DefSetup()

    def start_measure(self,
                      v_start: float = 5, v_stop: float = 25, v_step: float = 0.5):
        size = (v_stop - v_start)/v_step
        ampl = np.zeros(size, size)
        pulse_width = np.zeros(size, size)
        time_mid = []
        voltages = arange(v_start, v_stop, v_step)
        for i in voltages:
            self.pu.Voltage_Change_CH1(i)
            for j in voltages:
                self.pu.Voltage_Change_CH2(j)
                values = self.ocs.GetYData()
                ampl[i, j] = max(values)
                middle = 0.5*max(values)
                k = 0
                while k < len(values):
                    if values(k) < middle:
                        continue
                    else:
                        time_mid.append(values[k])
                width_pulse = time_mid[-1] - time_mid[0]
                pulse_width[i, j] = width_pulse
                pass
        return (voltages, ampl, width)

    def experiment_end(self):
        self.Rigol.End_of_Work()
        Oscilloscope_Agilent86100D.Reset()

    def pos_pulse_beg(self, waveform, ampl_plus, treshold_plus):
        return pos_time_start

    def pos_pulse_end(self, waveform, ampl_plus, treshold_plus):
        return pos_time_end

    def neg_pulse_beg(self, waveform):
        return neg_time_start

    def neg_pulse_end(self, waveform):
        return neg_time_end

if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    Rigol = PURigol(rm, 'TCPIP0::192.168.1.227::inst0::INSTR')  # The name of the PU in the experiment
    Rigol.Deafult_Setup_CH1()
    Rigol.Deafult_Setup_CH2()
    Agilent = Oscilloscope_Agilent86100D(rm, 'TCPIP0::192.168.1.5::inst0::INSTR')  # The name of the osc in the exp
    exp = Experiment()
    voltages, ampl, width = exp.ampl_width_map()
