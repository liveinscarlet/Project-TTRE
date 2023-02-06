import pyvisa
import tkinter as tk
import ttkthemes as ttk
from Apps.InstrumentControl.Rigol import PURigol
from Apps.Algorithms.Experiment import Experiment
from Apps.InstrumentControl.AgilentDCAX import OscilloscopeAgilent86100D

# Create resource managers
rm1 = pyvisa.ResourceManager()
rm2 = pyvisa.ResourceManager()
rm = pyvisa.ResourceManager()

# Create objects from classes
# osc = OscilloscopeAgilent86100D(rm)
# Rigol = PURigol(rm1)
# GWInstek = PUGW_Instek(rm2)

# The application design
window = tk.Tk()
window.title("Измерение параметров СКИ")
window.geometry("800x500")
style = ttk.ThemedStyle(window)
print(style.theme_names())
style.set_theme("arc")

# Buttons functions
def PURRigol_on():
    Rigol = PURigol(rm1)
    Rigol.default_setup_ch1()
    Rigol.default_setup_ch2()

# def GWInstek_on():
#     GWInstek.default_setup_ch1()
#     GWInstek.default_setup_ch2()

def Osc_on():
    osc = OscilloscopeAgilent86100D(rm2)
    osc.def_setup()

btn_PURigol_on = Button(window, text="Включить Rigol", command=PURRigol_on)
btn_GWInstek_on = Button(window, text="Включить GWInstek", command=GWInstek_on)
btn_Osc_on = Button(window, text="Включить осциллограф", command=Osc_on)
btn_PURigol_on.grid(column=5000, row=0)
btn_GWInstek_on.grid(column=5000, row=1)
btn_Osc_on.grid(column=6000, row=2)


window.mainloop()