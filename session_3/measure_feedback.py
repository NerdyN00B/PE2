import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
from MyDAQ_PID import MyDAQ_PID
import time

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

daq = MyDAQ_PID(setpoint=0.05,
                min_output=0,
                max_output=4,
                kp=0,ki=500, kd=0,
                feedback_rate=20,
                feedback_cycles=100,)

kps = np.linspace(10, 40, 10)

def longmeasure():
    data = []

    for kp in kps:
        daq = MyDAQ_PID(setpoint=0.1,
                min_output=0,
                max_output=4,
                kp=kp,ki=0, kd=0,
                feedback_rate=20,
                feedback_cycles=100,)
        daq.measure()
        data_i = np.concatenate(daq.data)
        data.append(data_i)
        np.save(savefile.replace('.npy', f'_{kp}'), data_i)
        time.sleep(1)
        del daq

    # for i, kp in enumerate(kps):
        # np.save(f"{savefile}_{kp}", data[i])
    
    error = daq.setpoint - data

    mean = np.mean(error, axis=0)
    std = np.std(error, axis=0)
    var = np.var(error, axis=0)

    fig, axs = plt.subplots(2, dpi=300, figsize=(6, 8))
    
    axs[0].errorbar(kps, np.abs(mean), label='absolute mean')
    print(mean)
    print(std)
    axs[1].scatter(kps, var, label='variance')
    print(var)

    for ax in axs:
        ax.set_xlabel('kp')
        ax.legend()
        
    axs[0].set_ylabel('absolute mean error')
    axs[1].set_ylabel('variance of error')

    fig.savefig(savefile.replace('.npy', '.pdf'))
    fig.savefig(savefile.replace('.npy', '.png'))

def quickmeasure():
    daq.measure()
    
    data = np.concatenate(daq.data)
    
    plt.plot(daq.setpoint-data)
    plt.show()
    
    np.save(savefile, data)

    # fig, ax = plt.subplots(dpi=300)
    
    # time = np.linspace(0, data.size / daq.samplerate, data.size)
    
    # ax.plot(time, data)
    # ax.hlines(daq.setpoint, 0, data.size / daq.samplerate,
    #           colors='r', linestyles='--')
    # ax.set_xlabel('time $t$ [$s$]')
    # ax.set_ylabel('Voltage $V$ [$V$]')
    
    # fig.savefig(savefile.replace('.npy', '.pdf'))
    # fig.savefig(savefile.replace('.npy', '.png'))

quickmeasure()
# longmeasure()