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

daq = md(200_000, name='myDAQ2')

data = daq.measure_step_response()

np.save(savefile, data)

transfer_functions, frequencies = daq.get_transfer_from_response(data, 0.8)

fig, *axs = daq.quickplot_from_response(transfer_functions[0], frequencies[0])

fig.savefig(savefile.replace('.npy', '.pdf'))
fig.savefig(savefile.replace('.npy', '.png'))

plt.show()