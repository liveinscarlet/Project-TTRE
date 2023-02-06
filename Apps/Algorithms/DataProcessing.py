import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Default params of the plots
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['font.size'] = '18'


class Plots(object):
    @staticmethod
    def maps(x, y, z):
        """
    Plots 3D-surface
        :param x: x-axes
        :param y: y-axes
        :param z: z-axes
        """
        fig = plt.figure(figsize=(41, 36))
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
        fig1 = plt.figure(figsize=(12, 10))
        plt.plot(x, y)
        plt.grid(True, which='major')
        plt.grid(True, which='minor')
        plt.minorticks_on()
        plt.xlabel('Время, сек')
        plt.ylabel('Напряжение, В')
        plt.title('Осциллограмма импульса')
        plt.xlim(0.3*10**(-7), 0.45*10**(-7))
        fig1.colorbar()
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
        fig, ax = plt.subplots(figsize=(8, 7))
        # ax.pcolormesh(-V1, V2, amples, cmap="jet", label="Амплитуды СКИ, В")
        ax.set_xlim(-27.5, -8)
        ax.set_ylim(8, 27.5)
        fig.colorbar(mappable=ax.pcolormesh(-V1, V2, amples * 10 ** 12, cmap="jet", vmax=250, vmin=170), label="длительности СКИ, пс")
        if is_positive:
            plt.xlabel("V1, накачка, В", fontsize=25)
            plt.ylabel("V2, рассасывание, В", fontsize=25)
        else:
            plt.xlabel("V1, рассасывание, В", fontsize=25)
            plt.ylabel("V2, накачка, В", fontsize=25)
        plt.show()

    @staticmethod
    def exp_plot(V1, V2, amples, width, width01, width07,
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
        fig.colorbar(mappable=ax1.pcolormesh(-V1, V2, amples, cmap="jet"))
        ax1.pcolormesh(-V1, V2, amples, cmap="jet")
        ax1.set_title("UWB pulse amplitudes", font="Times New Roman", fontsize=70)
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(41, 36))
        ax1.set_ylim(-5, -27.5)
        ax2.set_ylim(5, 27.5)
        ax3.set_ylim(5, 27.5)
        ax4.set_ylim(5, 27.5)
        ax1.set_xlim(27, 5)
        ax2.set_xlim(-27, -5)
        ax3.set_xlim(-27, -5)
        ax4.set_xlim(-27, -5)
        fig.colorbar(mappable=ax1.pcolormesh(V1, -V2, amples, cmap="jet"), label="Амплитуды СКИ, В")
        ax1.pcolormesh(V1, -V2, amples, cmap="jet")
        ax1.set_title("Амплитуды СКИ", font="Times New Roman", fontsize=70)
        if is_positive:
            ax1.set_xlabel("V1, накачка, В", font="Times New Roman", fontsize=60)
            ax1.set_ylabel("V2, рассасывание, В", font="Times New Roman", fontsize=60)
        else:
            ax1.set_xlabel("V1, рассасывание, В", font="Times New Roman", fontsize=60)
            ax1.set_ylabel("V2, накачка, В", font="Times New Roman", fontsize=60)
        plt.xlim(8, 27.5)
        plt.ylim(-27, -8)

        fig.colorbar(mappable=ax2.pcolormesh(-V1, V2, width * 10 ** 12, cmap="jet", vmax=170, vmin=100))
        ax2.set_title("UWB pulse width, level = 0.5", font="Times New Roman", fontsize=70)
        fig.colorbar(mappable=ax2.pcolormesh(V1, -V2, width * 10 ** 12, cmap="jet", vmin=160, vmax=250),
                     label="Длительность СКИ, пс")
        ax2.set_title("Длительность СКИ, уровень = 0.5", font="Times New Roman", fontsize=70)
        plt.xlim(8, 27.5)
        plt.ylim(-27, -8)
        if is_positive:
            ax2.set_xlabel("V1, накачка, В", font="Times New Roman", fontsize=60)
            ax2.set_ylabel("V2, рассасывание, В", font="Times New Roman", fontsize=60)
        else:
            ax2.set_xlabel("V1, рассасывание, В", font="Times New Roman", fontsize=60)
            ax2.set_ylabel("V2, накачка, В", font="Times New Roman", fontsize=60)

        fig.colorbar(mappable=ax3.pcolormesh(-V1, V2, abs(width01 * 10 ** 12), cmap="jet", vmin=80, vmax=110))
        ax3.set_title("UWB pulse width, level = 0.1", font="Times New Roman", fontsize=70)
        fig.colorbar(mappable=ax3.pcolormesh(V1, -V2, abs(width01 * 10 ** 12), cmap="jet", vmax=800, vmin=300),
                     label="Длительность СКИ, пс")
        ax3.set_title("Длительность СКИ, уровень = 0.1", font="Times New Roman", fontsize=70)
        plt.xlim(8, 27.5)
        plt.ylim(-27, -8)
        if is_positive:
            ax3.set_xlabel("V1, накачка, В", font="Times New Roman", fontsize=60)
            ax3.set_ylabel("V2, рассасывание, В", font="Times New Roman", fontsize=60)
        else:
            ax3.set_xlabel("V1, рассасывание, В", font="Times New Roman", fontsize=60)
            ax3.set_ylabel("V2, накачка, В", font="Times New Roman", fontsize=60)
        plt.xlim(8, 27.5)

        fig.colorbar(mappable=ax4.pcolormesh(-V1, V2, width07 * 10 ** 12, cmap="jet", vmax=450, vmin=90))
        ax4.set_title("UWB pulse width, level = 0.7", font="Times New Roman", fontsize=70)
        fig.colorbar(mappable=ax4.pcolormesh(V1, -V2, width07 * 10 ** 12, cmap="jet", vmax=180, vmin=120),
                     label="Длительность СКИ, пс")
        ax4.set_title("Длительность СКИ, уровень = 0.7", font="Times New Roman", fontsize=70)
        plt.xlim(8, 27.5)
        plt.ylim(-27, -8)
        if is_positive:
            ax4.set_xlabel("V1, накачка, В", font="Times New Roman", fontsize=60)
            ax4.set_ylabel("V2, рассасывание, В", font="Times New Roman", fontsize=60)
        else:
            ax4.set_xlabel("V1, рассасывание, В", font="Times New Roman", fontsize=60)
            ax4.set_ylabel("V2, накачка, В", font="Times New Roman", fontsize=60)
        plt.xlim(8, 27.5)
        plt.show()
        # plt.savefig("Full results")


if __name__ == "__main__":

    data1 = pd.read_csv(fr'C:\Projects\Project-TTRE\Apps\Waveforms\Neg_3SRD\ampls.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    data2 = pd.read_csv(fr'C:\Projects\Project-TTRE\Apps\Waveforms\Neg_3SRD\width.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    data3 = pd.read_csv(fr'C:\Projects\Project-TTRE\Apps\Waveforms\Neg_3SRD\width_long.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    data4 = pd.read_csv(fr'C:\Projects\Project-TTRE\Apps\Waveforms\Neg_3SRD\width_short.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    # times = pd.read_csv(r"D:\Учеба\ТТРЭ\Project\Project-TTRE\Apps\Waveforms\times_V115.0_V211.0.csv", sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    # amples = pd.read_csv(r"D:\Учеба\ТТРЭ\Project\Project-TTRE\Apps\Waveforms\waveform_V115.0_V211.0.csv", sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')

    data1 = pd.read_csv(r'amplitudes_array_plus.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    data2 = pd.read_csv(r'width_array_plus.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    data3 = pd.read_csv(r'D:\Учеба\ТТРЭ\Project\Project-TTRE\Result_array\pulse_width_full01.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    data4 = pd.read_csv(r'D:\Учеба\ТТРЭ\Project\Project-TTRE\Result_array\pulse_width_short07.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    # times = pd.read_csv(r"D:\Учеба\ТТРЭ\Project\Project-TTRE\Apps\Waveforms\times_V115.0_V211.0.csv", sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    # amples = pd.read_csv(r"D:\Учеба\ТТРЭ\Project\Project-TTRE\Apps\Waveforms\waveform_V115.0_V211.0.csv", sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    times_pulse = pd.read_csv(r'waveform_positive5.0_V25.0.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    amples_pulse = pd.read_csv(r'times_positiveV15.0_V25.0.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')

    width = data2.to_numpy()
    amplitudes = data1.to_numpy()
    width01 = data3.to_numpy()
    width07 = data4.to_numpy()

    x = np.arange(8, 28.25, 0.25)
    y = np.arange(8, 28, 0.25)

    times_pulse = times_pulse.to_numpy()
    amples_pulse = amples_pulse.to_numpy()


    x = np.arange(8, 28.3, 0.3)
    y = np.arange(8, 28, 0.3)

    Plots.like_spectrogram(x, y, data2, is_positive=True)

    # Plots.exp_plot(x, y, data1, data2, data3, data4, is_positive=False)
    # plt.plot(times, amples)
    # plt.grid(True, which="major", color='k')
    # plt.grid(True, which="minor", color='k')
    # plt.show()
    # fig = plt.figure(figsize=(26, 10))
    # plt.plot(x, amplitudes[0], label=f'E2 = {round(-y[0])}')
    # plt.plot(x, amplitudes[20], label=f'E2 = {round(-y[20])}')
    # plt.plot(x, amplitudes[10], label=f'E2 = {round(-y[10])}')
    # plt.plot(x, amplitudes[30], label=f'E2 = {round(-y[30])}')
    # plt.plot(x, amplitudes[40], label=f'E2 = {round(-y[40])}')
    # plt.plot(x, amplitudes[50], label=f'E2 = {round(-y[50])}')
    # plt.plot(x, amplitudes[60], label=f'E2 = {round(-y[60])}')
    # plt.plot(x, amplitudes[70], label=f'E2 = {round(-y[70])}')
    # plt.grid(True, which="major")
    # plt.grid(True, which="minor")
    # plt.legend()
    # plt.xlim(5, 27)
    # plt.show()
    #
    # fig2 = plt.figure(figsize=(26, 10))
    # plt.plot(-y, amplitudes[:, 0], label=f'E1 = {round(x[0])}')
    # plt.plot(-y, amplitudes[:, 20], label=f'E1 = {round(x[20])}')
    # plt.plot(-y, amplitudes[:, 10], label=f'E1 = {round(x[10])}')
    # plt.plot(-y, amplitudes[:, 40], label=f'E1 = {round(x[40])}')
    # plt.plot(-y, amplitudes[:, 50], label=f'E1 = {round(x[50])}')
    # plt.plot(-y, amplitudes[:, 60], label=f'E1 = {round(x[60])}')
    # plt.plot(-y, amplitudes[:, 70], label=f'E1 = {round(x[70])}')
    # plt.grid(True, which="major")
    # plt.grid(True, which="minor")
    # plt.legend()
    # plt.xlim(-27, -5)
    # plt.show()
