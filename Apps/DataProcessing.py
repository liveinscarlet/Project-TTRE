import numpy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import plot
plt.rcParams['font.family'] = 'monospace '


class Plots(object):
    def maps(self, x, y, z):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, cmap='inferno')
        ax.legend()
        plt.grid(True)
        plt.show()

    def time_maps(self, x, y):
        plt.plot(x, y)
        plt.grid(True, which='major')
        plt.grid(True, which='minor')
        plt.minorticks_on()
        plt.xlabel('Time, sec')

if __name__ == "__main__":
    x = np.linspace(0, 1, 1000)
    y = np.sin(10 * x)
    z = np.cos(50 * x)
    plt.plot(x, y)
