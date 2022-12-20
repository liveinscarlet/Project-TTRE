import matplotlib.pyplot as plt
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
                  threshold: float = 0.5,
                  is_positive: bool = True):
        ampl = [x if is_positive else -x for x in ampl_pulse]
        index_start = np.argmax(ampl)
        index_stop = np.argmax(ampl)
        level = max(ampl) * threshold
        time = time_pulse

        st = True
        while st:
            st = ampl[index_start] > level
            index_start -= 1

        st = True
        while st:
            st = ampl[index_stop] > level
            index_stop += 1

        # time_start = 0
        # for i, a in enumerate(ampl, start=0):
        #     if a > level and time_start == 0:
        #         time_start = time[i]
        #         break
        #
        # rev_ampl = list(reversed(ampl))
        # time_stop = 0
        # for i, a in enumerate(rev_ampl, start=0):
        #     if a > level and time_stop == 0:
        #         time_stop = time[-i]
        #         break

        dur = time[index_stop] - time[index_start]
        return dur

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
    osc.def_setup()
    time_pulse = exp.time()
    ampl = exp.ampl()
    voltages = np.arange(3, 28, 0.5)
    max_amp_full = np.array(5)
    size_zer = (len(voltages)+1, len(voltages)+1)
    max_amp = np.zeros(size_zer)
    pulse_width = np.zeros(size_zer)
    pulse_width_full01 = np.zeros(size_zer)
    pulse_width_short07 = np.zeros(size_zer)
    i, j = 0, 0

    ind_i = 0
    ind_j = 0
    for i in voltages:
        pu.v_change_1(i)
        for j in voltages:
            pu.v_change_2(j)
            time.sleep(1)
            ampl = exp.ampl()
            times = exp.time()
            timemax_coordinate = times[ampl.index(min(ampl))]
            if min(ampl) >= -0.5:
                osc.def_setup()
            else:
                osc.timebase_change(timemax_coordinate)
            duration2 = exp.time_meas(times, ampl, is_positive=False)
            max_amp[ind_i][ind_j] = min(ampl)
            pulse_width[ind_i][ind_j] = duration2
            pulse_width_full = exp.time_meas(times, ampl, 0.1, is_positive=False)
            pulse_width_short = exp.time_meas(times, ampl, 0.7, is_positive=False)
            pulse_width_full01[ind_i][ind_j] = pulse_width_full
            pulse_width_short07[ind_i][ind_j] = pulse_width_short
            np.savetxt(f"waveform_V1{i}_V2{j}.csv", ampl, delimiter=",")
            np.savetxt(f"times_V1{i}_V2{j}.csv", times, delimiter=",")
            print(f"Imp[{ind_i}][{ind_j}] on V1={i};V2={j} "
                  f"have amp={max_amp[ind_i][ind_j]:.1f}V;"
                  f"dur={pulse_width[ind_i][ind_j]*1e9:.3f}ns; "
                  f"dur full={pulse_width_full01[ind_i][ind_j]*1e9:.3f}ns; "
                  f"dur short={pulse_width_short07[ind_i][ind_j]*1e9:.3f}ns; ")
            ind_j += 1
        osc.def_setup()
        ind_j = 0
        ind_i += 1

    # Save data
    np.savetxt("amplitudes_array.csv", max_amp, delimiter=",")
    np.savetxt("width_array.csv", pulse_width, delimiter=",")
    np.savetxt("pulse_width_full01.csv", pulse_width_full01, delimiter=",")
    np.savetxt("pulse_width_short07.csv", pulse_width_short07, delimiter=",")


    Plots.like_spectrogram(voltages, voltages, max_amp)
    Plots.like_spectrogram(voltages, voltages, pulse_width)


    # Plots.maps(voltages, voltages, pulse_width)
    # exp.experiment_end()