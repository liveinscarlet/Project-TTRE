import numpy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import plot
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
    def time_maps(x, y):
        plt.plot(x, y)
        plt.grid(True, which='major')
        plt.grid(True, which='minor')
        ax.plot_surface(x, y, z, cmap='inferno')
        plt.minorticks_on()
        plt.xlabel('Time, sec')

if __name__ == "__main__":
    x = np.linspace(0, 1, 1000)
    y = np.sin(10 * x)
    z = np.cos(50 * x)
    plt.plot(x, y)
