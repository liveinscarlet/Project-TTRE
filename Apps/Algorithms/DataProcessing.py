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
        ax.plot_surface(x, y, cmap='inferno')
        plt.minorticks_on()
        plt.xlabel('Time, sec')

    @staticmethod
    def like_spectrogram(x):
        fig = plt.figure()
        plt.Axes.imshow(x, cmap='inferno')
        plt.show()

if __name__ == "__main__":
    # Experimental data
    data = ([[ 0, -0.262, -0.69, -10.752, -8.674, -3, -6.759, -6.346, -5.114,
-5.198, -5.361, -5.608, -5.689, -5.361, -5.608, -5.445],
[0, -0.433, -0.52, -11.837, -11.837, -5.445, -5.689, -7.905, -7.416,
-6.593, -6.183, -6.183, -6.43, -6.512, -6.84, -6.593],
[ 0, -0.262, -0.346, -12.333, -14.951, -9.522, -4.533, -7.826, -8.674,
-8.444, -7.826, -7.25, -7.25, -7.169, -7.25, -7.416],
[ 0, -0.262, -0.262, -12.898, -17.286, -13.184, -7.006, -6.675, -9.137,
-10.059, -9.366,-9.137, -8.521, -8.06, -8.444, -7.905],
[ 0, -0.346, -0.262, -11.905, -19.133, -16.377, -10.983, -6.512, -8.213,
-10.212, -10.904, -10.904, -10.059, -9.827, -9.366, -9.443],
[ 0, -0.262, -0.346, -12.473, -21.091, -19.787, -14.887, -9.058, -7.579,
-9.522, -10.983, -11.765, -11.694, -11.623, -11.409, -10.904],
[ 0, -0.262, -0.262, -11.837, -21.687, -22.01, -18.3, -12.898, -8.521,
-8.521, -10.52, -11.837, -12.83, -12.758, -12.758, -12.402],
[ 0, -0.262, -0.262, -11.126, -22.66, -24.325, -20.984, -16.767, -11.837,
-9.137, -9.674, -11.197, -12.048, -13.255, -13.82, -13.68 ],
[ 0, -0.262, -0.262, -10.599, -23.472, -25.619, -24.078, -19.907, -15.147,
-11.409, -9.674, -10.52, -11.694, -12.898, -13.82, -14.238],
[ 0, -0.262, -0.346, -9.674, -24.027, -27.355, -25.718, -23.092, -19.191,
-15.017, -11.977, -10.904, -11.409, -12.191, -13.326, -13.752],
[ 0, -0.346, -0.346, -8.982, -24.078, -29.143, -28.272, -25.817, -21.957,
-18.715, -15.147, -12.758, -11.765, -12.048, -12.687, -13.395],
[ 0, -0.262, -0.262, -7.905, -24.126, -29.961, -29.961, -28.593, -25.766
-22.12, -18.537, -15.211, -13.184, -12.758, -12.687, -13.184],
[ 0, -0.346, -0.346, -6.593, -23.146, -30.004, -31.616, -30.809, -28.364,
-24.226, -21.903, -18.119, -16.184, -14.434, -13.255, -13.609],
[ 0, -0.346, -0.262, -6.018, -23.199, -30.979, -33.016, -32.38, -30.259,
-27.31, -25.17, -21.74, -19.252, -17.22, -15.924, -14.824],
[ 0, -0.346, -0.262, -5.114, -22.497, -30.895, -33.964, -33.885, -32.591,
-30.513, -27.951, -24.277, -22.39, -20.497, -18.595, -16.897]])
    plt.Axes.imshow(data)