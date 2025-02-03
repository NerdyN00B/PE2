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

## Prompt loading and load data
root = tk.Tk()
root.withdraw()

dir = os.getcwd() + '/PE1/session_5'

file_path = filedialog.askopenfilename(filetypes=[('Numpy files', '.npy')],
                                        initialdir=dir,
                                        title='Select data file',
                                        )

data = np.load(file_path)

sq_fourier_1 = np.fft.fft(data)

window = np.hanning(len(data))
hanning_fourier_1 = np.fft.fft(data * window)

frequencies = np.fft.fftfreq(len(data), 1 / samplerate)

fig, ax = plt.subplots(figsize=(16, 9), dpi=300)

ax.scatter(frequencies[:len(frequencies) // 2],
           20*np.log10(np.abs(sq_fourier_1)[:len(frequencies) // 2]),
           label='Square window, 1s')

ax.scatter(frequencies[:len(frequencies) // 2],
           20*np.log10(np.abs(hanning_fourier_1)[:len(frequencies) // 2]),
           label='Hanning window, 1s')