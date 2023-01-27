import numpy as np
import pyvisa
import time
from DataProcessing import Plots
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

    @staticmethod
    def voltage_meas(voltages):
        """
    Finds amplitude of the pulse
        :param voltages: array of voltages from the oscilloscope
        :return: amplitude of the pulse, float
        """
        volt = max(voltages)
        return volt

    @staticmethod
    def time_meas(time_pulse: np.array,
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
            if index_start == 1:
                index_start = 0
                break
            st = ampl[index_start] > level
            index_start -= 1

        st = True
        while st:
            if index_stop == (len(ampl) - 1):
                index_stop == len(ampl) - 1
                break
            st = ampl[index_stop] > level
            index_stop += 1
        dur = time[index_stop] - time[index_start]
        return dur

    def experiment_end(self):
        """
    Turns everything off
        """
        self.pu.end_of_work()
        self.ocs.Reset()

    def experiment(self,
                   v_max: float = 28,
                   v_min: float = 5,
                   v_step: float = 0.5,
                   save_waveforms: bool = False,
                   save_results: bool = False,
                   show_plots: bool = False,
                   check_print: bool = True,
                   is_positive: bool = True):
        """
    Experimental functions, contains all experimental data and events
        :param v_max: max meaning of the voltage on the PU
        :param v_min: min meaning of the voltage on the PU
        :param v_step: voltage step
        :param save_waveforms: allows to save waveforms from the oscilloscope to folder Waveforms
        :param save_results: allows to save experimental results to folder Results_array
        :param show_plots: allows to show 2D plots with experimental results
        :param check_print: allows to print meanings of the voltages on the channels of the PU, amplitude
        of the pulse and it`s duration
        :param is_positive: sets polarity of the pulse
        """
        voltages = np.arange(v_min, v_max, v_step)

        size_zer = (len(voltages) + 1, len(voltages) + 1)
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
                ampl = self.ampl()
                times = self.time()
                timemax_coordinate = times[ampl.index(min(ampl))]

                # Dynamic range of time
                if min(ampl) >= -0.5:
                    osc.def_setup()
                else:
                    osc.timebase_change(timemax_coordinate)

                # Results calculation
                duration2 = self.time_meas(times, ampl, is_positive=False)
                max_amp[ind_i][ind_j] = min(ampl)
                pulse_width[ind_i][ind_j] = duration2
                pulse_width_full = self.time_meas(times, ampl, 0.1, is_positive=False)
                pulse_width_short = self.time_meas(times, ampl, 0.7, is_positive=False)
                pulse_width_full01[ind_i][ind_j] = pulse_width_full
                pulse_width_short07[ind_i][ind_j] = pulse_width_short

                # Save waveforms
                if save_waveforms:
                    np.savetxt(f"Waveforms.waveform_V1{i}_V2{j}.csv", ampl, delimiter=",")
                    np.savetxt(f"Waveforms.times_V1{i}_V2{j}.csv", times, delimiter=",")

                # Check print
                if check_print:
                    print(f"Imp[{ind_i}][{ind_j}] on V1={i};V2={j} "
                          f"have amp={max_amp[ind_i][ind_j]:.1f}V;"
                          f"dur={pulse_width[ind_i][ind_j] * 1e9:.3f}ns; "
                          f"dur full={pulse_width_full01[ind_i][ind_j] * 1e9:.3f}ns; "
                          f"dur short={pulse_width_short07[ind_i][ind_j] * 1e9:.3f}ns; ")
                ind_j += 1
            osc.def_setup()
            ind_j = 0
            ind_i += 1

        # Save data
        if save_results:
            np.savetxt(f"Result_array.amplitudes_array.csv", max_amp, delimiter=",")
            np.savetxt(f"Result_array.width_array.csv", pulse_width, delimiter=",")
            np.savetxt(f"Result_array.pulse_width_full01.csv", pulse_width_full01, delimiter=",")
            np.savetxt(f"Result_array.pulse_width_short07.csv", pulse_width_short07, delimiter=",")
            np.savetxt(f"Result_array.time_max_ampl.csv", time_max_ampl, delimiter=",")

        if show_plots:
            Plots.exp_plot()


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
    v_min = 5
    step = 0.3
    voltages = np.arange(v_min, v_max, step)

    size_zer = (len(voltages) + 1, len(voltages) + 1)
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
            timemax_coordinate = times[ampl.index(max(ampl))]

            # Dynamic range of time
            if max(ampl) <= 3:
                osc.def_setup()
            else:
                osc.timebase_change(timemax_coordinate)

            # Results calculation
            duration2 = exp.time_meas(times, ampl, is_positive=False)
            pulse_width_short = exp.time_meas(times, ampl, 0.7, is_positive=False)
            max_amp[ind_i][ind_j] = max(ampl)
            pulse_width[ind_i][ind_j] = duration2
            osc.timebase_change_short(timemax_coordinate)
            pulse_width_full = exp.time_meas(times, ampl, 0.1, is_positive=False)
            pulse_width_full01[ind_i][ind_j] = pulse_width_full
            pulse_width_short07[ind_i][ind_j] = pulse_width_short

            # Save waveforms
            np.savetxt(f"waveform_positive{i}_V2{j}.csv", ampl, delimiter=",")
            np.savetxt(f"times_positiveV1{i}_V2{j}.csv", times, delimiter=",")

            # Check print
            print(f"Imp[{ind_i}][{ind_j}] on V1={i};V2={j} "
                  f"have amp={max_amp[ind_i][ind_j]:.1f}V;"
                  f"dur={pulse_width[ind_i][ind_j] * 1e9:.3f}ns; "
                  f"dur full={pulse_width_full01[ind_i][ind_j] * 1e9:.3f}ns; "
                  f"dur short={pulse_width_short07[ind_i][ind_j] * 1e9:.3f}ns; ")
            ind_j += 1
        osc.def_setup()
        ind_j = 0
        ind_i += 1

    # Save data
    np.savetxt(f"amplitudes_array_plus.csv", max_amp, delimiter=",")
    np.savetxt(f"width_array_minus2.csv", pulse_width, delimiter=",")
    np.savetxt(f"pulse_width_full01_minus2.csv", pulse_width_full01, delimiter=",")
    np.savetxt(f"pulse_width_short07_minus2.csv", pulse_width_short07, delimiter=",")
    np.savetxt(f"time_max_ampl_minus2.csv", time_max_ampl, delimiter=",")
