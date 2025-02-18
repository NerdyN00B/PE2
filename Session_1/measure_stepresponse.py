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

data = daq.measure_step_response(wait=1, duration=1)
# print(data.shape)

daq.write([0, 0, 0])

np.save(savefile, data)

transfer_functions, frequencies = daq.get_transfer_from_response(data, 0.1,
                                                                 is_step=True)

fig, ax = daq.quickplot_from_response(transfer_functions[0], frequencies[0])

# fig, ax = plt.subplots(dpi=300)

# ax.scatter(np.fft.rfftfreq(data[1][0].size, 1/200_000), abs(np.fft.rfft(data[1][0])))
# ax.set_xscale('log')
# ax.set_xlim(0, 10000)
# ax.scatter(np.fft.rfftfreq(data[0][0].size, 1/200_000), abs(np.fft.rfft(data[0][0])))
# ax.set_yscale('log')
fig.savefig(savefile.replace('.npy', '.pdf'))
fig.savefig(savefile.replace('.npy', '.png'))
