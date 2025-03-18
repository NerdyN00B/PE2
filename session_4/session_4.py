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


def measure_impulse():
    dir = os.getcwd()
    dir += '/session_4'

    root = tk.Tk()
    root.withdraw()

    savefile = filedialog.asksaveasfilename(filetypes=[('Numpy files', '.npy')],
                                            defaultextension='.npy',
                                            initialdir=dir,
                                            title='Save raw data as',
                                            confirmoverwrite=True,
                                            )

    daq = md(200_000, name='myDAQ3')

    data = daq.measure_impulse_response(duration=0.1, ammount=5)
    np.save(savefile, data)
    
    transfers, frequencies = daq.get_transfer_from_response(data, 0.1,
                                                            is_step=False)
    
    fig, *axs = md.make_bode_plot(dpi=300, layout='tight', figsize=(16, 9))

    gain_ax, phase_ax, polar_ax = axs
    
    mean_gain, std_gain, mean_phase, std_phase = md.analyse_transfer(transfers)
    
    gain_ax.errorbar(frequencies, mean_gain, yerr=std_gain*2, fmt='ok',
                     label='Data $\pm 2\sigma$', capsize=2)
    gain_ax.set_xscale('log')
    gain_ax.set_xlabel('Frequency [Hz]')
    gain_ax.set_ylabel('Gain [dB]')
    gain_ax.set_title('Magnitude bode plot')
    
    phase_ax.errorbar(frequencies, mean_phase, yerr=std_phase*2, fmt='ok',
                      label='Data $\pm 2\sigma$', capsize=2)
    phase_ax.set_xscale('log')
    phase_ax.set_xlabel('Frequency [Hz]')
    phase_ax.set_ylabel('Phase [rad]')
    phase_ax.set_title('Phase bode plot')
    
    polar_ax.scatter(abs(transfers), np.angle(transfers), c='k', label='Data')
    polar_ax.set_xlabel('Magnitude')
    polar_ax.set_ylabel('Phase [deg]')
    polar_ax.set_title('Polar plot')
    
    # fig.savefig(savefile.replace('.npy', '.pdf'))
    fig.savefig(savefile.replace('.npy', '.png'))


def meusure_long():
    dir = os.getcwd()
    dir += '/session_4'

    root = tk.Tk()
    root.withdraw()

    savefile = filedialog.asksaveasfilename(filetypes=[('Numpy files', '.npy')],
                                            defaultextension='.npy',
                                            initialdir=dir,
                                            title='Save raw data as',
                                            confirmoverwrite=True,
                                            )

    daq = md(200_000, name='myDAQ3')

    frequencies = np.logspace(1, 5, 10, dtype=int)
    data = daq.measure_spectrum(frequencies, duration=1, repeat = 5)
    np.save(savefile, data)
    np.save(data.replace('.npy', '_frequencies.npy'), frequencies)
    
    transfers = daq.get_transfer_functions(data, frequencies, 5)
    
    mean_gain, std_gain, mean_phase, std_phase = md.analyse_transfer(transfers)
    
    fig, *axs = md.make_bode_plot(dpi=300, layout='tight', figsize=(16, 9))
    gain_ax, phase_ax, polar_ax = axs
    
    gain_ax.errorbar(frequencies, mean_gain, yerr=std_gain*2, fmt='ok',
                     label='Data $\pm 2\sigma$', capsize=2)
    gain_ax.set_xscale('log')
    gain_ax.set_xlabel('Frequency [Hz]')
    gain_ax.set_ylabel('Gain [dB]')
    gain_ax.set_title('Magnitude bode plot')
    
    phase_ax.errorbar(frequencies, mean_phase, yerr=std_phase*2, fmt='ok',
                      label='Data $\pm 2\sigma$', capsize=2)
    phase_ax.set_xscale('log')
    phase_ax.set_xlabel('Frequency [Hz]')
    phase_ax.set_ylabel('Phase [rad]')
    phase_ax.set_title('Phase bode plot')
    
    polar_ax.scatter(10**(mean_gain/20), mean_phase, c='k', label='Data')
    polar_ax.set_xlabel('Magnitude')
    polar_ax.set_ylabel('Phase [deg]')
    polar_ax.set_title('Polar plot')
    
    # fig.savefig(savefile.replace('.npy', '.pdf'))
    fig.savefig(savefile.replace('.npy', '.png'))


def make_bode():
    root = tk.Tk()
    root.withdraw()
    
    dir = os.getcwd() + '/session_4'
    
    file_path = filedialog.askopenfilename(filetypes=[('Numpy files', '.npy')],
                                            initialdir=dir,
                                            title='Select data file',
                                            )
    
    data = np.load(file_path)
    
    transfers, frequencies = md.get_transfer_from_response(data, 0.1,
                                                            is_step=False)
    
    # frequencies = np.load(file_path.replace('.npy', '_frequencies.npy'))
    # transfers = md.get_transfer_functions(data, frequencies, 5)
    
    mean_gain, std_gain, mean_phase, std_phase = md.analyse_transfer(transfers)
    
    fig, *axs = md.make_bode_plot(dpi=300, layout='tight', figsize=(16, 9))

    gain_ax, phase_ax, polar_ax = axs
    
    gain_ax.errorbar(frequencies, mean_gain, yerr=std_gain*2, fmt='ok',
                     label='Data $\pm 2\sigma$', capsize=2)
    gain_ax.set_xscale('log')
    gain_ax.set_xlabel('Frequency [Hz]')
    gain_ax.set_ylabel('Gain [dB]')
    gain_ax.set_title('Magnitude bode plot')
    
    phase_ax.errorbar(frequencies, mean_phase, yerr=std_phase*2, fmt='ok',
                      label='Data $\pm 2\sigma$', capsize=2)
    phase_ax.set_xscale('log')
    phase_ax.set_xlabel('Frequency [Hz]')
    phase_ax.set_ylabel('Phase [rad]')
    phase_ax.set_title('Phase bode plot')
    
    polar_ax.scatter(10**(mean_gain/20), mean_phase, c='k', label='Data')
    polar_ax.set_xlabel('Magnitude')
    polar_ax.set_ylabel('Phase [deg]')
    polar_ax.set_title('Polar plot')
    
    # fig.savefig(file_path.replace('.npy', '.pdf'))
    fig.savefig(file_path.replace('.npy', '.png'))


if __name__ == '__main__':
    measure_impulse()
    # meusure_long()
    # make_bode()