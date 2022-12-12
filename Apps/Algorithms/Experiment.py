from numpy import arange
import numpy as np
import pyvisa
import time
from AgilentDCAX import OscilloscopeAgilent86100D
from Rigol import PURigol
from DataProcessing import Plots

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
        self.ocs = OscilloscopeAgilent86100D(self.rm, addr_osc)  # The name of the osc in the exp

        self.pu.default_setup_ch1()
        self.pu.default_setup_ch2()
        self.ocs.def_setup()

    def ampl(self):
        ampl = self.ocs.GetYData()
        return ampl

    def time(self):
        time_pulse = self.ocs.GetXdata()
        return time_pulse

    def voltage_change(self,
                     v_start: float = 5,
                     v_stop: float = 25,
                     v_step: float = 0.5):
        size = (v_stop - v_start) / v_step
        ampl = np.zeros(size, size)
        i, j = 0, 0
        voltages = arange(v_start, v_stop, v_step)
        for i in voltages:
            self.pu.v_change_1(i)
            for j in voltages:
                self.pu.v_change_2(j)
                values = self.ocs.GetYData()
                ampl[i, j] = max(values)
                pass
        return voltages, ampl

    @staticmethod
    def voltage_meas(voltages):
        volt = max(voltages)
        return volt

    def time_meas(self,
                  time_pulse,
                  ampl_pulse,
                  threshold: float = 0.5):
        global time_start, time_end
        level = max(ampl_pulse) * threshold
        ampl = np.array(ampl_pulse)
        time = np.array(time_pulse)
        for i in ampl:
            if i >= level:
                time_start = time[ampl_pulse.index(i)]
                break
        ampl = list(reversed(ampl_pulse))
        for j in ampl:
            if j >= level:
                time_end = time[ampl_pulse.index(j)]
                break
        return time_start, time_end

    def experiment_end(self):
        self.pu.end_of_work()
        self.ocs.Reset()


if __name__ == "__main__":
    rm1 = pyvisa.ResourceManager()
    rm2 = pyvisa.ResourceManager()
    rm = pyvisa.ResourceManager()
    osc = OscilloscopeAgilent86100D(rm1, 'TCPIP0::192.168.1.5::inst0::INSTR')
    pu = PURigol(rm2, 'TCPIP0::192.168.1.227::inst0::INSTR')
    exp = Experiment(rm)
    time_pulse = exp.time()
    ampl = exp.ampl()
    voltages = np.linspace(1, 15, 16)
    max_amp_full = np.array(5)
    size_zer = (16, 16)
    max_amp = np.zeros(size_zer)
    pulse_width = np.zeros(size_zer)
    i, j = 0, 0

    for i in voltages:
        pu.v_change_1(i)
        for j in voltages:
            pu.v_change_2(j)
            ampl = exp.ampl()
            time.sleep(0.5)
            time_imp = exp.time_meas(time_pulse, ampl)
            duration = osc.width()
            max_amp[int(i)][int(j)] = min(ampl)
            pulse_width[int(i)][int(j)] = duration
        j = 0

    print(max_amp)
    print(pulse_width)
    Plots.maps(voltages, voltages, max_amp)
    Plots.maps(voltages, voltages, pulse_width)
    # exp.experiment_end()