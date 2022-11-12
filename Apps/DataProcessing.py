import numpy
import matplotlib as plt

class Plots(object):
    def maps(self, x, y, z):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, cmap='inferno')
        ax.legend()
        plt.show()
