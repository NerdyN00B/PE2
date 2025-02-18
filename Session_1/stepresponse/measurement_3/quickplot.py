import numpy as np
import matplotlib.pyplot as plt

data = np.load("C:/Users/masla/Documents/School/Natuurkunde WO/Jaar 2/PE2/Session_1/stepresponse/measurement_3/measurement_3.npy")

step = data[0][0]
responnse = data[1][0]

plt.plot(step)
plt.plot(responnse)

plt.show()