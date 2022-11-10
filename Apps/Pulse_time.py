from numpy import arange
import numpy as np
import tkinter
import pyvisa
import matplotlib as plt
import time
from AgilentDCAX import OscilloscopeAgilent86100D
from Rigol import PURigol

waveform = []
ampl_plus = max(waveform)
treshold_plus = 0.1*ampl_plus
ampl_minus = min(waveform)
treshold_minus = 0.1*ampl_minus

def pos_pulse_beg (waveform, ampl_plus, treshold_plus):
    return pos_time_start

def pos_pulse_end (waveform, ampl_plus, treshold_plus):
    return pos_time_end

def neg_pulse_beg (waveform):
    return neg_time_start

def neg_pulse_end(waveform):
    return neg_time_end