import pyvisa
from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedStyle
from Rigol import PURigol, PUGW_Instek
from Experiment import Experiment
from AgilentDCAX import OscilloscopeAgilent86100D

# Create resource managers
rm1 = pyvisa.ResourceManager()
rm2 = pyvisa.ResourceManager()
rm = pyvisa.ResourceManager()

# Create objects from classes
# osc = OscilloscopeAgilent86100D(rm)
# Rigol = PURigol(rm1)
# GWInstek = PUGW_Instek(rm2)

# The application design
window = Tk()
window.title("Измерение параметров СКИ")
window.geometry("800x500")
style = ThemedStyle(window)
print(style.theme_names())
style.set_theme("arc")

# Buttons functions
def PURRigol_on():
    Rigol.default_setup_ch1()
    Rigol.default_setup_ch2()

def GWInstek_on():
    GWInstek.default_setup_ch1()
    GWInstek.default_setup_ch2()

def Osc_on():
    osc.def_setup()

btn_PURigol_on = Button(window, text="Включить Rigol", command=PURRigol_on)
btn_GWInstek_on = Button(window, text="Включить GWInstek", command=GWInstek_on)
btn_Osc_on = Button(window, text="Включить осциллограф", command=Osc_on)
btn_PURigol_on.grid(column=5000, row=0)
btn_GWInstek_on.grid(column=5000, row=1)
btn_Osc_on.grid(column=6000, row=2)


window.mainloop()


import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure

# LARGE_FONT = ("Verdana", 12)
#
#
# class SeaofBTCapp(tk.Tk):
#
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#
#         tk.Tk.iconbitmap(self, default="clienticon.ico")
#         tk.Tk.wm_title(self, "Sea of BTC client")
#
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#
#         self.frames = {}
#
#         for F in (StartPage, PageOne, PageTwo, PageThree):
#             frame = F(container, self)
#
#             self.frames[F] = frame
#
#             frame.grid(row=0, column=0, sticky="nsew")
#
#         self.show_frame(StartPage)
#
#     def show_frame(self, cont):
#         frame = self.frames[cont]
#         frame.tkraise()

# Tried to show plots
# class StartPage(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Start Page", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)
#
#         button = ttk.Button(self, text="Visit Page 1",
#                             command=lambda: controller.show_frame(PageOne))
#         button.pack()
#
#         button2 = ttk.Button(self, text="Visit Page 2",
#                              command=lambda: controller.show_frame(PageTwo))
#         button2.pack()
#
#         button3 = ttk.Button(self, text="Graph Page",
#                              command=lambda: controller.show_frame(PageThree))
#         button3.pack()
#
#
# class PageOne(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)
#
#         button1 = ttk.Button(self, text="Back to Home",
#                              command=lambda: controller.show_frame(StartPage))
#         button1.pack()
#
#         button2 = ttk.Button(self, text="Page Two",
#                              command=lambda: controller.show_frame(PageTwo))
#         button2.pack()
#
#
# class PageTwo(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)
#
#         button1 = ttk.Button(self, text="Back to Home",
#                              command=lambda: controller.show_frame(StartPage))
#         button1.pack()
#
#         button2 = ttk.Button(self, text="Page One",
#                              command=lambda: controller.show_frame(PageOne))
#         button2.pack()
#
#
# class PageThree(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)
#
#         button1 = ttk.Button(self, text="Back to Home",
#                              command=lambda: controller.show_frame(StartPage))
#         button1.pack()
#
#         f = Figure(figsize=(5, 5), dpi=100)
#         a = f.add_subplot(111)
#         a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
#
#         canvas = FigureCanvasTkAgg(f, self)
#         canvas.show()
#         canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
#
#         toolbar = NavigationToolbar2TkAgg(canvas, self)
#         toolbar.update()
#         canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#
# app = SeaofBTCapp()
# app.mainloop()