import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
from MyDAQ_PID import MyDAQ_PID


index = 0
setpoint = 0.7
samplerate = 200_000

dir = os.getcwd()
dir += '/session_3'

root = tk.Tk()
root.withdraw()

loadfile = filedialog.askopenfilename(filetypes=[('Numpy files', '.npy')],
                                        initialdir=dir,
                                        title='Select data file',
                                        )

data = np.load(loadfile)[index]

fig, ax = plt.subplots(dpi=300)

error = setpoint - data

time = np.linspace(0, data.size() / samplerate, data.size())

ax.plot(time, error)
ax.set_xlabel('time [s]')
ax.set_ylabel('error')
plt.show()