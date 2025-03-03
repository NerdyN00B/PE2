import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
from MyDAQ_PID import MyDAQ_PID

dir = os.getcwd()
dir += '/session_3'

root = tk.Tk()
root.withdraw()

savefile = filedialog.asksaveasfilename(filetypes=[('Numpy files', '.npy')],
                                            defaultextension='.npy',
                                            initialdir=dir,
                                            title='Save raw data as',
                                            confirmoverwrite=True,
                                            )

daq = MyDAQ_PID(setpoint=0.7,
                min_output=0,
                max_output=4,
                kp=0,ki=0, kd=0,
                feedback_rate=20,
                feedback_cycles=100,)

kps = np.linspace(0, 1, 10)

def longmeasure():
    data = []

    for kp in kps:
        daq.kp = kp
        data.append(daq.measure())

    data = np.stack(data)
    np.save(savefile, data)
    
    error = daq.setpoint - data

    mean = np.mean(error, axis=0)
    var = np.var(error, axis=0)

    fig, ax = plt.subplots( dpi=300, figsize=(6, 8))

    ax.scatter(kps, np.abs(mean), label='absolute mean')
    ax.scatter(kps, var, label='variance')

    ax.set_xlabel('kp')
    ax.set_ylabel('value')
    ax.legend()

    fig.savefig(savefile.replace('.npy', '.pdf'))
    fig.savefig(savefile.replace('.npy', '.png'))

def quickmeasure():
    data = daq.measure()
    np.save(savefile, data)

    fig, ax = plt.subplots(dpi=300)
    ax.plot(data)
    ax.hlines(daq.setpoint, 0, len(data), colors='r', linestyles='--')
    ax.set_xlabel('time')
    ax.set_ylabel('value')
    
    fig.savefig(savefile.replace('.npy', '.pdf'))
    fig.savefig(savefile.replace('.npy', '.png'))

quickmeasure()
# longmeasure()