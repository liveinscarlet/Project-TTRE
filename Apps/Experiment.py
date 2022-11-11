from numpy import arange
import tkinter
import pyvisa
import time
from AgilentDCAX import OscilloscopeAgilent86100D
from Rigol import PURigol

V_start, V_max = 0, 10
step = 0.5
Voltages = arange(V_start, V_max, step)  # Array of positive voltages
waveform = []  # Signal from the oscilloscope
time_dom = []  # x axes
amplitude = []  # y axes
max_amp = []  # Meanings of the amplitudes of the pulses
pulse_width = []  # Array of pulses width


class Experiment(PURigol, OscilloscopeAgilent86100D):
    def __int__(self):
        rm = pyvisa.ResourceManager()
        Rigol = PURigol(rm, 'TCPIP0::192.168.1.227::inst0::INSTR')  # The name of the PU in the experiment
        Agilent = OscilloscopeAgilent86100D(rm, 'TCPIP0::192.168.1.5::inst0::INSTR')  # The name of the osc in the exp
        Rigol.Deafult_Setup_CH1()
        time.sleep(1)  # Just in case
        Rigol.Deafult_Setup_CH2()
        Agilent.DefSetup()

    def ampl_width_map(self, v_min, v_max, step):
        v_min = float(input('Voltage to begin'))
        v_max = float(input('Maximum voltage'))
        step = float(input('Step for voltages'))
        ampl = []
        voltages = arange(v_min, v_max, step)
        for i in Voltages:
            PURigol.Voltage_Change_CH1(i)
            for j in Voltages:
                PURigol.Voltage_Change_CH2(j)
                values = OscilloscopeAgilent86100D.GetYData()
                ampl.append(max(values))
                middle = 0.5*max(values)
                k = 0
                time_mid = []
                while k < len(values):
                    if values(k)<middle:
                        continue
                    else:
                        time_mid.append(values[k])
                width = time_mid[-1] - time_mid[0]
                pulse_width.append(width)
                pass
        return (voltages, ampl, width)

    # def experiment_end(self):
    #     PURigol.End_of_Work()
    #     OscilloscopeAgilent86100D.Reset()
    #
    # def pos_pulse_beg(waveform, ampl_plus, treshold_plus):
    #     return pos_time_start
    #
    # def pos_pulse_end(waveform, ampl_plus, treshold_plus):
    #     return pos_time_end
    #
    # def neg_pulse_beg(waveform):
    #     return neg_time_start

    # def neg_pulse_end(waveform):
    #     return neg_time_end

# if __name__ == "__main__":
