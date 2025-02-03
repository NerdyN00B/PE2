import sys
import os
import inspect

parentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from mydaq import MyDAQ as md
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import tkinter as tk
from tkinter import filedialog

def low_pass_transfer(omega, omega_0):
    return 1 / (1 + 1j * omega / omega_0)

def gain_transfer(omega, omega_0, offset):
    return 20 * np.log10(np.abs(low_pass_transfer(omega, omega_0))) + offset

def phase_transfer(omega, omega_0, offset):
    return np.angle(low_pass_transfer(omega, omega_0)) + offset


## Default values
resistance = 100e3
capacitance = 1.5e-9
cutoff = 1/(resistance * capacitance)
cutoff_hz = cutoff / (2 * np.pi)


## Prompt loading and load data
root = tk.Tk()
root.withdraw()

dir = os.getcwd() + '/Session_1'

file_path = filedialog.askopenfilename(filetypes=[('Numpy files', '.npy')],
                                        initialdir=dir,
                                        title='Select data file',
                                        )

data = np.load(file_path)

## Analyse data
transfers, frequencies = md.get_transfer_from_response(data, 0.8)

transfer = transfers[0][:len(frequencies[0])//2]
frequency = frequencies[0][:len(frequencies[0])//2]

fig, *axs = md.make_bode_plot(dpi=300, layout='tight', figsize=(16, 9))

gain_ax, phase_ax, polar_ax = axs

gain_ax.scatter(frequency, 20*np.log10(np.abs(transfer)), c='k', label='Data')
gain_ax.set_xscale('log')
gain_ax.set_xlabel('Frequency [Hz]')
gain_ax.set_ylabel('Gain [dB]')
gain_ax.set_title('Magnitude bode plot')

phase_ax.scatter(frequency, np.angle(transfer), c='k', label='Data')
phase_ax.set_xscale('log')
phase_ax.set_xlabel('Frequency [Hz]')
phase_ax.set_ylabel('Phase [rad]')
phase_ax.set_title('Phase bode plot')

polar_ax.scatter(abs(transfer), np.angle(transfer), c='k', label='Data')
polar_ax.set_xlabel('Magnitude')
polar_ax.set_ylabel('Phase [deg]')
polar_ax.set_title('Polar plot')

omega = frequency * 2 * np.pi

## Fit data
theoretical = low_pass_transfer(omega, cutoff)
gain_ax.plot(frequency, 20*np.log10(np.abs(theoretical)),
             c='r', linestyle='dashed', label='Theoretical')

phase_ax.plot(frequency, np.angle(theoretical),
              c='r', linestyle='dashed', label='Theoretical')

polar_ax.plot(abs(theoretical), np.angle(theoretical),
              c='r', linestyle='dashed', label='Theoretical')
polar_ax.legend()

popt_gain, pcov_gain = curve_fit(gain_transfer,
                                 omega,
                                 20*np.log10(np.abs(transfer)),
                                 p0=[cutoff, 0])

popt_phase, pcov_phase = curve_fit(phase_transfer,
                                   omega,
                                   np.angle(transfer),
                                   p0=[cutoff, 0])

gain_ax.plot(frequency, gain_transfer(omega, *popt_gain),
             c='k', linestyle='dashed', label='Fit')
gain_ax.legend()

phase_ax.plot(frequency, phase_transfer(omega, *popt_phase),
              c='k', linestyle='dashed', label='Fit')
phase_ax.legend()

fig.savefig(file_path.replace('.npy', '_analysed.pdf'))
fig.savefig(file_path.replace('.npy', '_analysed.png'))

plt.show()
