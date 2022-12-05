import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 1000)
y = np.sin(10 * x)

plt.plot(x, y)
plt.show()