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
from scipy.optimize import curve_fit

R = 100e3
C = 1e-6

def theory(freq):
    return -1j * freq * R * C

def fitfunc(freq, RC):
    omega = 2 * np.pi * freq
    transfer = -1j * omega * RC
    return 20 * np.log10(np.abs(transfer))

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

    daq = md(200_000, name='myDAQ4')

    data = daq.measure_impulse_response(duration=0.1, amount=5)
    np.save(savefile, data)
    
    transfers, frequencies = daq.get_transfer_from_response(data, 0.1,
                                                            is_step=False)
    
    fig, *axs = md.make_bode_plot(dpi=300, layout='tight', figsize=(16, 9))
    
    frequencies = frequencies[0]

    gain_ax, phase_ax, polar_ax = axs
    
    mean_gain, std_gain, mean_phase, std_phase = md.analyse_transfer(transfers)
    
    gain_ax.errorbar(frequencies, mean_gain, yerr=std_gain*2, fmt='ok',
                     label=r'Data $\pm 2\sigma$', capsize=2)
    gain_ax.set_xscale('log')
    gain_ax.set_xlabel('Frequency [Hz]')
    gain_ax.set_ylabel('Gain [dB]')
    gain_ax.set_title('Magnitude bode plot')
    
    phase_ax.errorbar(frequencies, mean_phase, yerr=std_phase*2, fmt='ok',
                      label=r'Data $\pm 2\sigma$', capsize=2)
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

    daq = md(200_000, name='myDAQ4')

    frequencies = np.logspace(1, 5, 50, dtype=int)  
    data = daq.measure_spectrum(frequencies, amplitude=0.05,
                                duration=1, repeat = 3)
    np.save(savefile, data)
    np.save(savefile.replace('.npy', '_frequencies.npy'), frequencies)
    
    transfers = daq.get_transfer_functions(data, frequencies, 3)
    
    mean_gain, std_gain, mean_phase, std_phase = md.analyse_transfer(transfers)
    
    fig, *axs = md.make_bode_plot(dpi=300, layout='tight', figsize=(16, 9))
    gain_ax, phase_ax, polar_ax = axs
    
    gain_ax.errorbar(frequencies, mean_gain, yerr=std_gain*2, fmt='ok',
                     label=r'Data $\pm 2\sigma$', capsize=2)
    gain_ax.plot(frequencies,
                 20*np.log10(np.abs(theory(frequencies*2*np.pi))),
                 'r', label='Theory')

    gain_ax.set_xscale('log')
    gain_ax.set_xlabel('Frequency [Hz]')
    gain_ax.set_ylabel('Gain [dB]')
    gain_ax.set_title('Magnitude bode plot')
    
    phase_ax.errorbar(frequencies, mean_phase, yerr=std_phase*2, fmt='ok',
                      label=r'Data $\pm 2\sigma$', capsize=2)
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
    
    # transfers, frequencies = md.get_transfer_from_response(data, 0.1,
    #                                                         is_step=False)
    
    # frequencies = frequencies[0]
    
    frequencies = np.load(file_path.replace('.npy', '_frequencies.npy'))
    transfers = md.get_transfer_functions(data, frequencies, 3)
    
    mean_gain, std_gain, mean_phase, std_phase = md.analyse_transfer(transfers)
    
    fig, *axs = md.make_bode_plot(dpi=300, layout='tight', figsize=(16, 9))

    gain_ax, phase_ax, polar_ax = axs
    
    gain_ax.errorbar(frequencies, mean_gain, yerr=std_gain*2, fmt='ok',
                     label=r'Data $\pm 2\sigma$', capsize=2)
    gain_ax.plot(frequencies,
        20*np.log10(np.abs(theory(frequencies*2*np.pi))),
                 'r', label='Theory')
    # gain_ax.plot(frequencies, mean_gain, 'ok')
    # gain_ax.fill_between(frequencies, mean_gain-std_gain*2, mean_gain+std_gain*2,
    #                      color='r', alpha=0.5, label=r'$\pm 2\sigma$')
    
    gain_ax.set_xscale('log')
    gain_ax.set_xlabel('Frequency [Hz]')
    gain_ax.set_ylabel('Gain [dB]')
    gain_ax.set_title('Magnitude bode plot')
    gain_ax.legend()
    
    
    phase_ax.errorbar(frequencies, mean_phase, yerr=std_phase*2, fmt='ok',
                      label=r'Data $\pm 2\sigma$', capsize=2)
    
    # phase_ax.plot(frequencies, mean_phase, 'ok')
    # phase_ax.fill_between(frequencies, mean_phase-std_phase*2, mean_phase+std_phase*2,
    #                       color='r', alpha=0.5, label=r'$\pm 2\sigma$')
    phase_ax.set_xscale('log')
    phase_ax.set_xlabel('Frequency [Hz]')
    phase_ax.set_ylabel('Phase [rad]')
    phase_ax.set_title('Phase bode plot')
    phase_ax.legend()
    
    
    
    polar_ax.scatter(10**(mean_gain/20), mean_phase, c='k', label='Data')
    polar_ax.set_xlabel('Magnitude')
    polar_ax.set_ylabel('Phase [deg]')
    polar_ax.set_title('Polar plot')
    
    max_idx = np.argmax(mean_gain)
    print(f'Peak gain at {frequencies[max_idx]} Hz'.rjust(50))
    print(f'Peak gain: {mean_gain[max_idx]} dB'.rjust(50))
    print(f'Peak std: {std_gain[max_idx]} dB'.rjust(50))
    
    # fig.savefig(file_path.replace('.npy', '.pdf'))
    fig.savefig(file_path.replace('.npy', '.png'))


def fit_data():
    root = tk.Tk()
    root.withdraw()
    
    dir = os.getcwd() + '/session_4'
    
    file_path = filedialog.askopenfilename(filetypes=[('Numpy files', '.npy')],
                                            initialdir=dir,
                                            title='Select data file',
                                            )
    
    data = np.load(file_path)
    
    frequencies = np.load(file_path.replace('.npy', '_frequencies.npy'))
    transfers = md.get_transfer_functions(data, frequencies, 3)
    
    mean_gain, std_gain, mean_phase, std_phase = md.analyse_transfer(transfers)
    
    fit = []
    error = []
    for i in range(mean_gain.size-1):
        freq = frequencies[:i+1]
        gain = mean_gain[:i+1]
        std = std_gain[:i+1]
        
        popt, pcov = curve_fit(fitfunc, freq, gain, sigma=std, p0=[R * C])
        fit.append(popt[0])
        error.append(np.sqrt(np.diag(pcov))[0])
    
    fit = np.array(fit)
    error = np.array(error)
    
    fig, ax = plt.subplots(dpi=300, figsize=(16, 9))
    ax.errorbar(frequencies[1:], fit, yerr=2*error, fmt='ok',
                label=r'fit $\pm 2\sigma$', capsize=2)
    
    best = np.argmin(error[5:])
    best +=5
    print(f'Best fit at {frequencies[1+best]} Hz')
    print(f'RC = {fit[best]} s')
    print(f'Error = {error[best]} s')
    print(best+1)
    ax.scatter(frequencies[1+best], fit[best], c='r', label='Best fit', s=100)
    
    ax.set_xscale('log')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('RC [s]')
    ax.set_title('RC fit')
    ax.legend()
    
    fig.savefig(file_path.replace('.npy', '_fit.png'))
    print(fit)
    print(error)
    print(frequencies[1:])

def final_fit():
    root = tk.Tk()
    root.withdraw()
    
    dir = os.getcwd() + '/session_4'
    
    file_path = filedialog.askopenfilename(filetypes=[('Numpy files', '.npy')],
                                            initialdir=dir,
                                            title='Select data file',
                                            )
    
    data = np.load(file_path)
    
    frequencies = np.load(file_path.replace('.npy', '_frequencies.npy'))
    transfers = md.get_transfer_functions(data, frequencies, 3)
    
    mean_gain, std_gain, mean_phase, std_phase = md.analyse_transfer(transfers)
    
    idx = 21
    
    fitfreq = frequencies[:idx]
    fitgain = mean_gain[:idx]
    fitstd = std_gain[:idx]
    restfreq = frequencies[idx:]
    restgain = mean_gain[idx:]
    reststd = std_gain[idx:]
    
    popt, pcov = curve_fit(fitfunc, fitfreq, fitgain, sigma=fitstd, p0=[R * C])
    fit = popt[0]
    error = np.sqrt(np.diag(pcov))[0]
    
    fig, ax = plt.subplots(dpi=300, layout='tight')
    ax.errorbar(fitfreq, fitgain, yerr=2*fitstd, fmt='ok',
                label=r'data to fit to $\pm 2\sigma$', capsize=2,
                markersize=3)
    ax.errorbar(restfreq, restgain, yerr=2*reststd, fmt='ob',
                label=r'data not fit $\pm 2\sigma$', capsize=2,
                markersize=3)
    ax.plot(frequencies, fitfunc(frequencies, fit), ':r', 
            label=f'Fit RC=({fit:.2e} $\\pm$ {error:.2e}) s')
    
    ax.set_xscale('log')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Gain [dB]')
    ax.set_title('Magnitude bode plot')
    ax.legend()
    
    fig.savefig(file_path.replace('.npy', '_final_fit.png'))
    

if __name__ == '__main__':
    # measure_impulse()
    # meusure_long()
    # make_bode()
    # fit_data()
    final_fit()