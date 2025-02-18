import sys
import os
import inspect

parentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from mydaq_long import MyDAQ_Long
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

first = False
centerfreq = 1024
duration = 60
new = False

daq = MyDAQ_Long()

def find_closest_idx(array, value):
    return (np.abs(array - value)).argmin()


def quickplot(hanning=True):
    possible_freqs = [512, 1024, 2048, 4096, 8192]
    time, data = daq.capture(duration=2, samplerate=200_000)
    
    if hanning:
        window = np.hanning(len(data))
        data = data * window
    
    fourier = np.fft.fft(data)
    freq = np.fft.fftfreq(len(data), 1/200_000)
    
    gain = 20 * np.log10(abs(fourier))
    
    fig, ax = plt.subplots(dpi=300, layout='tight')
    
    ax.scatter(freq[:len(freq)//2], gain[:len(freq)//2],
               c='k',
               marker='.'
               )
    ax.set_xscale('log')
    ax.set_xlabel('Frequency $f$ [$Hz$]')
    ax.set_ylabel('amplitude $A$ [$dB$]')
    
    ax.vlines(possible_freqs, np.min(gain), np.max(gain),
              colors='r',
              linestyle='--',
              )
    # ax.set_xlim(0, 10_000)
    ax.set_xticks(possible_freqs)
    
    timestring = datetime.now().strftime("%d-%b-%Y(%H%M%S)")
    savething = parentdir + '\\session_2\\figures\\' + 'soundtest_' + timestring
    fig.savefig(savething + '.pdf')
    fig.savefig(savething + '.png')
    
    return fig, ax


def longmeasure(center_freq, duration, hanning=True, new=True):
    if new:
    
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
        
        time, data = daq.capture(duration=duration, samplerate=200_000)
        
        np.save(savefile, data)
    else:
        root = tk.Tk()
        root.withdraw()

        dir = os.getcwd() + '/session_2'

        savefile = filedialog.askopenfilename(filetypes=[('Numpy files', '.npy')],
                                                initialdir=dir,
                                                title='Select data file',
                                                )
        data = np.load(savefile)
        
    if hanning:
        window = np.hanning(len(data))
        data = data * window
    
    fourier = np.fft.fft(data)
    freq = np.fft.fftfreq(len(data), 1/200_000)
    
    gain = 20 * np.log10(abs(fourier))
    
    # fig, ax = plt.subplots(dpi=300)
    
    possible_freqs = [512, 1024, 2048, 4096, 8192]
    
    for possible_freq in possible_freqs:
        
        center_idx = find_closest_idx(freq, possible_freq)
        
        fig, ax = plt.subplots(dpi=300)
        ax.vlines(possible_freqs, np.min(gain), np.max(gain),
                colors='r',
                linestyle='--',
                )
        
        ax.scatter(freq, gain,
                c='k',
                marker='.',
                s=10,
                )
        
        
        ax.set_xscale('log')
        ax.set_xlim(freq[center_idx-10], freq[center_idx+10])
        
        ax.set_xlabel('Frequency $f$ [$Hz$]')
        ax.set_ylabel('amplitude $A$ [$dB$]')
        
        # fig.savefig(savefile.replace('.npy', '.pdf'))
        fig.savefig(savefile.replace('.npy', f'_{possible_freq}.png'))
    
    return

if __name__ == '__main__':
    if first:
        fig, ax = quickplot()
    else:
        longmeasure(centerfreq, duration, new=new)