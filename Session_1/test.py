import numpy as np
import matplotlib.pyplot as plt


sr = 200_000
time = np.arange(0, 0.01, 1/sr)

rc = 1000 * 2 * np.pi

signal = 1 - np.exp(- time * rc)

# plt.plot(time, signal)

fourier = np.fft.rfft(signal)
freq = np.fft.rfftfreq(signal.size, 1/sr)

fourier = fourier * 2j * np.pi * freq

plt.plot(freq, 20*np.log10(abs(fourier)))
plt.xscale('log')

plt.show()