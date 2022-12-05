from numpy import arange
import numpy as np
import tkinter
import pyvisa
import time
from AgilentDCAX import OscilloscopeAgilent86100D
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
        self.ocs = OscilloscopeAgilent86100D(rm, addr_osc)  # The name of the osc in the exp

        self.pu.Deafult_Setup_CH1()
        self.pu.Deafult_Setup_CH2()
        self.ocs.DefSetup()

    def ampl(self):
        ampl = self.ocs.GetYData()
        return ampl

    def time(self):
        time_pulse = self.ocs.GetXdata()
        return time_pulse

    def voltage_meas(self,
                     v_start: float = 5,
                     v_stop: float = 25,
                     v_step: float = 0.5):
        size = (v_stop - v_start) / v_step
        ampl = np.zeros(size, size)
        voltages = arange(v_start, v_stop, v_step)
        for i in voltages:
            self.pu.Voltage_Change_CH1(i)
            for j in voltages:
                self.pu.Voltage_Change_CH2(j)
                values = self.ocs.GetYData()
                ampl[i, j] = max(values)
                pass
        return voltages, ampl

    def time_meas(self,
                  time_pulse,
                  ampl_pulse,
                  threshold: float = 0.5):
        global time_start, time_end
        level = max(ampl_pulse) * threshold
        for i in ampl_pulse:
            if i >= level:
                time_start = time_pulse[ampl_pulse.index(i)]
            break
        ampl_pulse = ampl_pulse.reversed()
        for j in ampl_pulse:
            if j >= level:
                time_end = time_pulse[ampl_pulse.index(j)]
            break
        return time_start, time_end

    def experiment_end(self):
        self.pu.End_of_Work()
        self.ocs.Reset()


if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    exp = Experiment(rm)
    check = np.array(2)
    check = exp.time_meas(exp.ampl(), exp.time())
    print(check)
