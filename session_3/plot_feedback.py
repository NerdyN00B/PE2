import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
from MyDAQ_PID import MyDAQ_PID


index = 0
setpoint = 0.1
samplerate = 200_000

dir = os.getcwd()
dir += '/session_3'

root = tk.Tk()
root.withdraw()

loadfile = filedialog.askopenfilename(filetypes=[('Numpy files', '.npy')],
                                        initialdir=dir,
                                        title='Select data file',
                                        )

def plot_feedback():
    data = np.load(loadfile)

    fig, ax = plt.subplots(dpi=300)

    error = setpoint - data

    time = np.linspace(0, data.size / samplerate, data.size)

    ax.plot(time, error, c='k', linewidth=0.5)
    ax.set_xlabel('time [s]')
    ax.set_ylabel('error')
    # plt.show()
    fig.savefig(loadfile.replace('.npy', '.png'))

def plot_stability(n):
    data = []
    data.append(np.load(loadfile))
    for i in n[1:]:
        loader = loadfile.replace(f'_{n[0]}', f'_{i}')
        data.append(np.load(loader))
    
    mean = []
    std = []
    var = []
    
    for i in range(len(n)):
        error = setpoint - data[i]
        mean.append(np.mean(error))
        std.append(np.std(error))
        var.append(np.var(error))
    
    fig, ax = plt.subplots(2, dpi=300, layout='tight')
    
    ax[0].errorbar(n, np.abs(mean), yerr=std, label='mean',
                   fmt='ok', capsize=2)
    ax[0].set_xlabel('$K_I$')
    ax[0].set_xscale('log')
    ax[0].set_ylabel('absolute mean error')
    
    ax[1].scatter(n, var, label='variance', c='k')
    ax[1].set_xlabel('$K_I$')
    ax[1].set_xscale('log')
    ax[1].set_ylabel('variance')
    
    # print(mean)
    # print(std)
    # print(var)
    
    fig.savefig(loadfile.replace(f'_{n[0]}.npy', '.png'))
    
    
    
    
def calc_mean_var():
    data = np.load(loadfile)
    error = setpoint - data
    print(np.mean(error))
    print(np.std(data))
    print(np.var(error))

# plot_stability([5, 10, 15, 20, 25, 30, 35, 40, 100, 500, 1000])
calc_mean_var()
# plot_feedback()