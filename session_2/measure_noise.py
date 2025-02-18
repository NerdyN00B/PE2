import sys
import os
import inspect

parentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from rigol import RigolOscilloscope
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from scipy.signal import find_peaks, periodogram

# TODO: CALCULATE NOISE SPECTRAL DENSITY

test = True
n_measurements = 1000
n_bins = 50

extra = False

scope = RigolOscilloscope()


def center_bins(bin_edges):
    c_bins = []
    for i in range(bin_edges.size - 1):
        c_bins.append((bin_edges[i] + bin_edges[i+1]) / 2)
        return np.array(c_bins)


def single_measurement():
    time, voltage = scope.captureChannel1()
    peaks = find_peaks(voltage,
                       height=None,
                       threshold=None,
                       distance=None,
                       )
    return time, voltage, peaks


def plot_single(time, voltage, peaks):
    fig, ax = plt.subplots(dpi=300, layout='tight')
    ax.plot(time, voltage, 
            c='k',
            label='Oscilloscope signal'
            )
    ax.scatter(time[peaks], voltage[peaks],
               c='r',
               marker='o',
               label='Peaks'
               )
    ax.set_xlabel('time $t$ [$s$]')
    ax.set_ylabel('voltage $V$ [$V$]')
    ax.legend()
    
    timestring = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
    savething = parentdir + 'session_2//figures//' + 'scopetest_' + timestring
    fig.savefig(savething + '.pdf')
    fig.savefig(savething + '.png')
    return fig, ax


def full_measurement(n_measurements=1000, n_bins=50):
    dir = os.getcwd()
    dir += '/session_2'

    root = tk.Tk()
    root.withdraw()

    savefile = filedialog.asksaveasfilename(filetypes=[('Numpy files', '.npy')],
                                            defaultextension='.npy',
                                            initialdir=dir,
                                            title='Save raw data as',
                                            confirmoverwrite=True,
                                            )
    
    times, voltages, n_peaks = [], [], []
    for _ in range(n_measurements):
        time, voltage, peaks = single_measurement()
        times.append(time)
        voltages.append(voltage)
        n_peaks.append(peaks.size)

    times = np.asarray(times)
    voltages = np.asarray(voltages)
    n_peaks = np.asarray(n_peaks)
    
    np.save(savefile, np.stack((times, voltages, n_peaks)))
    
    mean = np.mean(n_peaks)
    std = np.std(n_peaks)
    print("mean =\n\t", mean)
    print("std = \n\t", std)
    
    hist, bin_edges = np.histogram(n_peaks, n_bins)
    bins = center_bins(bin_edges)
    fig, ax = plt.subplots(dpi=300, layout='tight')
    
    ax.hist(hist, bins,
            color='k',
            label=f"mean = {mean:.2f}, std = {std:.2f}")
    ax.set_xlabel('number of peaks $N_{peaks}$')
    ax.set_ylabel('number of measurements $N_{measure}$')
    ax.legend()
    
    fig.savefig(savefile.replace('.npy', '.pdf'))
    fig.savefig(savefile.replace('.npy', '.png'))
    return fig, ax


def noise_spectral_density():
    root = tk.Tk()
    root.withdraw()

    dir = os.getcwd() + '/Session_1'

    file_path = filedialog.askopenfilename(filetypes=[('Numpy files', '.npy')],
                                            initialdir=dir,
                                            title='Select data file',
                                            )
    
    data = np.load(file_path)
    time = data[0]
    voltage = data[1]
    
    f, Pxx = periodogram(voltage, fs=200_000)
    average_Pxx = np.mean(Pxx, axis=0)
    
    fig, ax = plt.subplots()
    ax.scatter(f, average_Pxx,
               c='k',
               marker='.'
               )
    ax.set_xscale('log')
    ax.set_xlabel('Frequency $f$ [$Hz$]')
    ax.set_ylabel('Power spectral density $PSD$ [$V^2/Hz$]')
    
    fig.savefig(file_path.replace('.npy', '_PSD.pdf'))
    fig.savefig(file_path.replace('.npy', '_PSD.png'))    


if __name__ == "__main__":
    if test:
        fig, ax = plot_single(single_measurement())
        plt.show()
    elif not test and not extra:
        fig, ax = full_measurement(n_measurements, n_bins)
    elif extra:
        noise_spectral_density()