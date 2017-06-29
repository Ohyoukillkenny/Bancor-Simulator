import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

mu, sigma = 0, 0.3
x = np.linspace(-5, 5, 500)
y = 1/(sigma * np.sqrt(2 * np.pi))*np.exp(-(x-mu)**2/(2*sigma**2))

fig, ax = plt.subplots()
ax.fill(x, y, zorder=10, alpha = 0.5)
ax.grid(True, zorder=5)
plt.show()

