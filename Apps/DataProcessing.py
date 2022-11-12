import numpy
import matplotlib as plt
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
        fig = plt.figure()
        plt.plt(x, y)
        plt.grid(True, which='major')
        plt.grid(True, which='minor')
        plt.minorticks_on()
        plt.xlabel('Time, sec')


