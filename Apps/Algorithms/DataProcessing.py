import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Default params of the plots
plt.rcParams['font.family'] = 'Times New Roman'
plt.rc('font', size=40)

class Plots(object):
    @staticmethod
    def maps(x, y, z):
        """
    Plots 3D-surface
        :param x: x-axes
        :param y: y-axes
        :param z: z-axes
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.grid(True, which='major')
        plt.grid(True, which='minor')
        ax.plot_surface(x, y, z, cmap='inferno')
        ax.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_waveform(x, y):
        """
    Plots a waveform from the oscilloscope
        :param x: time samples
        :param y: amplitude samples
        """
        plt.plot(x, y)
        plt.grid(True, which='major')
        plt.grid(True, which='minor')
        plt.minorticks_on()
        plt.xlabel('Time, sec')
        plt.ylabel('Voltage, V')
        plt.title('Waveform')
        plt.show()

    @staticmethod
    def like_spectrogram(V1, V2, amples,
                         is_positive: bool = True):
        """
    Plots an RGB pic with voltages and amplitude of the pulse
        :param V1: voltage on the first channel of the PU
        :param V2: voltage pn the second channel of the PU
        :param amples: measured amplitudes of the pulses
        :param is_positive: sets polarity of the pulse
        """
        fig, ax = plt.subplots()
        ax.pcolormesh(V1, -V2, amples, cmap="gist_gray")
        fig.colorbar(mappable=ax.pcolormesh(V1, -V2, amples, cmap="jet"))
        if is_positive:
            plt.xlabel("V1, накачка, В")
            plt.ylabel("V2, рассасывание, В")
        else:
            plt.xlabel("V1, рассасывание, В")
            plt.ylabel("V2, накачка, В")
        plt.show()

    @staticmethod
    def exp_plot (V1, V2, amples, width, width01, width07,
                      is_positive: bool = True):
        """
    Plots not only pic for amplitudes, but also for width with different thresholds
        :param V1: voltage on the first channel of the PU
        :param V2: voltage pn the second channel of the PU
        :param amples: measured amplitudes of the pulses
        :param width: measured width of the pulses, threshold = 0.5
        :param width01: measured width of the pulses, threshold = 0.1
        :param width07: measured width of the pulses, threshold = 0.7
        :param is_positive: sets polarity of the pulse
        """
        fig, ((ax1, ax2) , (ax3, ax4)) = plt.subplots(2, 2, figsize=(40, 32))
        fig.colorbar(mappable=ax1.pcolormesh(V1, -V2, amples, cmap="jet", vmax=-6))
        ax1.pcolormesh(V1, -V2, amples, cmap="jet")
        ax1.set_title("UWB pulse amplitudes", font="Times New Roman", fontsize=70)
        if is_positive:
            ax1.set_xlabel("V1, накачка, В", font="Times New Roman", fontsize=60)
            ax1.set_ylabel("V2, рассасывание, В", font="Times New Roman", fontsize=60)
        else:
            ax1.set_xlabel("V1, рассасывание, В", font="Times New Roman", fontsize=60)
            ax1.set_ylabel("V2, накачка, В", font="Times New Roman", fontsize=60)

        fig.colorbar(mappable=ax2.pcolormesh(V1, -V2, width * 10 ** 12, cmap="jet", vmax=220, vmin=150))
        ax2.set_title("UWB pulse width, level = 0.5", font="Times New Roman", fontsize=70)
        if is_positive:
            ax2.set_xlabel("V1, накачка, В", font="Times New Roman", fontsize=60)
            ax2.set_ylabel("V2, рассасывание, В", font="Times New Roman", fontsize=60)
        else:
            ax2.set_xlabel("V1, рассасывание, В", font="Times New Roman", fontsize=60)
            ax2.set_ylabel("V2, накачка, В", font="Times New Roman", fontsize=60)

        fig.colorbar(mappable=ax3.pcolormesh(V1, -V2, abs(width01 * 10 ** 12), cmap="jet", vmin=200, vmax=650))
        ax3.set_title("UWB pulse width, level = 0.1", font="Times New Roman", fontsize=70)
        if is_positive:
            ax3.set_xlabel("V1, накачка, В", font="Times New Roman", fontsize=60)
            ax3.set_ylabel("V2, рассасывание, В", font="Times New Roman", fontsize=60)
        else:
            ax3.set_xlabel("V1, рассасывание, В", font="Times New Roman", fontsize=60)
            ax3.set_ylabel("V2, накачка, В", font="Times New Roman", fontsize=60)

        fig.colorbar(mappable=ax4.pcolormesh(V1, -V2, width07 * 10 ** 12, cmap="jet", vmax=150, vmin=90))
        ax4.set_title("UWB pulse width, level = 0.7", font="Times New Roman", fontsize=70)
        if is_positive:
            ax4.set_xlabel("V1, накачка, В", font="Times New Roman", fontsize=60)
            ax4.set_ylabel("V2, рассасывание, В", font="Times New Roman", fontsize=60)
        else:
            ax4.set_xlabel("V1, рассасывание, В", font="Times New Roman", fontsize=60)
            ax4.set_ylabel("V2, накачка, В", font="Times New Roman", fontsize=60)
        plt.show()
        # plt.savefig("Full results")


if __name__ == "__main__":
    data1 = pd.read_csv('width_array0.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    data2 = pd.read_csv('amplitudes_array0.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    data3 = pd.read_csv('pulse_width_full010.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    data4 = pd.read_csv('pulse_width_short070.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    times = pd.read_csv(r"D:\Учеба\ТТРЭ\Project\Project-TTRE\Apps\Waveforms\times_V115.0_V211.0.csv", sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    amples = pd.read_csv(r"D:\Учеба\ТТРЭ\Project\Project-TTRE\Apps\Waveforms\waveform_V115.0_V211.0.csv", sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')

    width = data1.to_numpy()
    amplitudes = data2.to_numpy()
    width01 = data3.to_numpy()
    width07 = data4.to_numpy()
    x = np.arange(5, 28.3, 0.3)
    y = np.arange(5, 28, 0.3)
    # plt.plot(times, amples)
    # plt.grid(True, which="major", color='k')
    # plt.grid(True, which="minor", color='k')
    # plt.show()
    Plots.exp_plot(x, y, amplitudes, width, width01, width07, is_positive=False)

