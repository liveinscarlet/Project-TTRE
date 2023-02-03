import matplotlib.pyplot as plt
from numpy import arange
import numpy as np
import pyvisa
import time
from Apps.InstrumentControl.AgilentDCAX import OscilloscopeAgilent86100D
from Apps.InstrumentControl.Rigol import PURigol

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
        """
    Extracts Y-samples from the oscilloscope
        :return: np.array with Y-samples
        """
        ampl = self.ocs.get_y_data()
        return ampl

    def time(self):
        """
    Extracts X-samples from the oscilloscope
        :return: np.array with X-samples
        """
        time_pulse = self.ocs.get_x_data()
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
                values = self.ocs.get_y_data()
                ampl[i, j] = max(values)
                pass
        return voltages, ampl

    @staticmethod
    def voltage_meas(voltages):
        """
    Finds amplitude of the pulse
        :param voltages: array of voltages from the oscilloscope
        :return: amplitude of the pulse, float
        """
        volt = min(voltages)
        return volt

    def time_meas(self,
                  time_pulse: np.array,
                  ampl_pulse: np.array,
                  threshold: float = 0.5,
                  is_positive: bool = True):
        """
    Measures width if the pulse
        :param time_pulse: X-data samples
        :param ampl_pulse: Y-data samples
        :param threshold: threshold of the amplitude of the pulse to measure width
        :param is_positive: sets polarity of the pulse
        :return: width of the pulse, float
        """
        ampl = [x if is_positive else -x for x in ampl_pulse]
        index_start = np.argmax(ampl)
        index_stop = np.argmax(ampl)
        level = max(ampl) * threshold
        time = time_pulse

        st = True
        while st:
            st = ampl[index_start] > level
            index_start -= 1
            if index_start == 0:
                index_start = 2
                break

        st = True
        while st:
            st = ampl[index_stop] > level
            index_stop += 1
            if index_stop == len(ampl):
                index_stop = len(ampl) - 2
                break
        dur = time[index_stop] - time[index_start]
        return dur

    def experiment_end(self):
        """
    Turns everything off
        """
        self.pu.end_of_work()
        self.ocs.Reset()


if __name__ == "__main__":
    # Resource managers for VISA communication
    rm1 = pyvisa.ResourceManager()
    rm2 = pyvisa.ResourceManager()
    rm = pyvisa.ResourceManager()

    # Creation of the objects for classes
    osc = OscilloscopeAgilent86100D(rm1, 'TCPIP0::192.168.1.5::inst0::INSTR')
    pu = PURigol(rm2, 'TCPIP0::192.168.1.227::inst0::INSTR')
    exp = Experiment(rm)
    osc.def_setup()

    # Creation of the arrays and variables
    time_pulse = exp.time()
    ampl = exp.ampl()

    # Voltage settings
    v_max = 28
    v_min = 8
    step = 0.25
    voltages = np.arange(v_min, v_max, step)

    size_zer = (len(voltages)+1, len(voltages)+1)
    max_amp = np.zeros(size_zer)
    pulse_width = np.zeros(size_zer)
    pulse_width_full01 = np.zeros(size_zer)
    pulse_width_short07 = np.zeros(size_zer)
    time_max_ampl = np.zeros(size_zer)

    # index declaration
    i, j = 0, 0
    ind_i = 0
    ind_j = 0

    # Experimental cycle
    for i in voltages:
        pu.v_change_1(i)
        for j in voltages:
            pu.v_change_2(j)
            time.sleep(0.5)

            # Data extraction
            ampl = exp.ampl()
            times = exp.time()
            timemax_coordinate = times[ampl.index(min(ampl))]

            # Dynamic range of time
            if min(ampl) >= -0.2:
                osc.def_setup()
            else:
                osc.timebase_change(timemax_coordinate)

            # Results calculation
            duration2 = exp.time_meas(times, ampl, is_positive=False)
            max_amp[ind_i][ind_j] = min(ampl)
            pulse_width[ind_i][ind_j] = duration2
            pulse_width_full = exp.time_meas(times, ampl, 0.1, is_positive=False)
            pulse_width_short = exp.time_meas(times, ampl, 0.7, is_positive=False)
            pulse_width_full01[ind_i][ind_j] = pulse_width_full
            pulse_width_short07[ind_i][ind_j] = pulse_width_short

            # Save waveforms
            np.savetxt(fr"C:\Projects\Project-TTRE\Apps\Waveforms\Neg_3SRD\amplsV{[i]}_V{j}.csv", ampl, delimiter=",")
            np.savetxt(fr"C:\Projects\Project-TTRE\Apps\Waveforms\Neg_3SRD\times_V1{i}_V2{j}.csv", times, delimiter=",")

            # Check print
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
    np.savetxt(r"C:\Projects\Project-TTRE\Apps\Waveforms\Neg_3SRD\ampls.csv", max_amp, delimiter=",")
    np.savetxt(r"C:\Projects\Project-TTRE\Apps\Waveforms\Neg_3SRD\width.csv", pulse_width, delimiter=",")
    np.savetxt(r"C:\Projects\Project-TTRE\Apps\Waveforms\Neg_3SRD\width_short.csv", pulse_width_full01, delimiter=",")
    np.savetxt(r"C:\Projects\Project-TTRE\Apps\Waveforms\Neg_3SRD\width_long.csv", pulse_width_short07, delimiter=",")
    np.savetxt(r"C:\Projects\Project-TTRE\Apps\Waveforms\Neg_3SRD\wtime_max_ampl.csv", time_max_ampl, delimiter=",")
