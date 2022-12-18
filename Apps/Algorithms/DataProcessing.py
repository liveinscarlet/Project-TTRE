import numpy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import plot
from numpy import ndarray
import pandas as pd

plt.rcParams['font.family'] = 'monospace '


class Plots(object):
    @staticmethod
    def maps(x, y, z):
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
        plt.plot(x, y)
        plt.grid(True, which='major')
        plt.grid(True, which='minor')
        plt.minorticks_on()
        plt.xlabel('Time, sec')
        plt.ylabel('Voltage, V')
        plt.title('Waveform')

    @staticmethod
    def like_spectrogram(V1, V2, amples,
                         is_positive: bool = True):
        fig, ax = plt.subplots()
        ax.pcolormesh(V1, -V2, amples, cmap="gist_gray")
        fig.colorbar(mappable=ax.pcolormesh(V1, -V2, amples, cmap="gist_gray"))
        if is_positive:
            plt.xlabel("V1, накачка, В")
            plt.ylabel("V2, рассасывание, В")
        else:
            plt.xlabel("V1, рассасывание, В")
            plt.ylabel("V2, накачка, В")
        plt.title("UWB pulse amplitudes")
        plt.show()


if __name__ == "__main__":
    data = pd.read_csv('./amplitudes_array.csv', sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')
    z = data.to_numpy()
    x = np.arange(3, 28.5, 0.5)
    y = np.arange(3, 28, 0.5)
    Plots.like_spectrogram(x, y, z, False)

