import matplotlib.pyplot as plt
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
        plt.plot(x, y)
        plt.grid(True, which='major')
        plt.grid(True, which='minor')
        plt.minorticks_on()
        plt.xlabel('Time, sec')

if __name__ == "__main__":
    pll = Plots()
    pll.time_maps([1,2,3,4,5], [3,3,3,3,4])
