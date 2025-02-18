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

## Prompt save file
dir = os.getcwd()
dir += '/Session_6'

root = tk.Tk()
root.withdraw()

savefile = filedialog.asksaveasfilename(filetypes=[('Numpy files', '.npy')],
                                         defaultextension='.npy',
                                         initialdir=dir,
                                         title='Save raw data as',
                                         confirmoverwrite=True,
                                         )


daq = md(200_000, name='myDAQ3')

data = daq.read(1, channel='ai0')

np.save(savefile, data)

fig = plt.figure()
ax, ax1 = fig.subplots(2, 1)

ax.plot(data)
ax1.plot(abs(np.fft.fft(data)))
ax1.set_xscale('log')
plt.show()
