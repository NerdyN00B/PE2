import sys
import os
import inspect

parentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from mydaq import MyDAQ as md
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

samplerate = 200_000
duration = 1

window_time = 0.5

n_samples = int(samplerate * window_time)

## Prompt loading and load data
root = tk.Tk()
root.withdraw()

dir = os.getcwd() + '/PE1/session_5'

file_path = filedialog.askopenfilename(filetypes=[('Numpy files', '.npy')],
                                        initialdir=dir,
                                        title='Select data file',
                                        )

data = np.load(file_path)

data = data[:n_samples]

sq_fourier_1 = np.fft.fft(data)

window = np.hanning(len(data))
hanning_fourier_1 = np.fft.fft(data * window)

frequencies = np.fft.fftfreq(len(data), 1 / samplerate)

idx = md.find_nearest_idx(frequencies, 440)
range = 100

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

ax.plot(frequencies[idx - range:idx + range],
           20*np.log10(np.abs(sq_fourier_1)[idx - range:idx + range]),
           label=f'Square window, {window_time}s', marker='.')

ax.plot(frequencies[idx - range:idx + range],
           20*np.log10(np.abs(hanning_fourier_1)[idx - range:idx + range]),
           label=f'Hanning window, {window_time}s', marker='.')
ax.set_title(f'Tuning fork frequency analysis with a window of {window_time} seconds')

ax.set_xscale('log')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude (dB)')
ax.legend()

fig.savefig(file_path.replace('.npy', f'_analysed_{window_time}s.pdf'))
fig.savefig(file_path.replace('.npy', f'_analysed_{window_time}.png'))