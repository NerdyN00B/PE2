import sys
import os
import inspect

parentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from mydaq import MyDAQ as md
import numpy as np
import matplotlib.pyplot as plt

def low_pass_transfer(omega, omega_0):
    return 1 / (1 + 1j * omega / omega_0)


resistance = 100e3
capacitance = 1.5e-9
cutoff = 1/(resistance * capacitance)

omega = np.logspace(0, 6, 1000)


fig, gain_ax, phase_ax, polar_ax = md.make_bode_plot(dpi=300,
                                                     figsize=(16, 9),
                                                     layout='tight',
                                                     )

md.plot_gain(gain_ax,
             omega,
             20*np.log10(np.abs(low_pass_transfer(omega, cutoff))),
             freq_label='Frequency $\omega$ [$rad/s$]',
             c='k',
             label='Transfer function'
             )
gain_ax.vlines(cutoff,
               np.min(20*np.log10(np.abs(low_pass_transfer(omega, cutoff)))),
               0,
               colors='r',
               linestyles='dashed',
               label='Cutoff frequency'
               )
gain_ax.legend()

md.plot_phase(phase_ax,
              omega, np.angle(low_pass_transfer(omega, cutoff)),
              freq_label='Frequency $\omega$ [$rad/s$]',
              c='k',
              label='Transfer function'
              )
phase_ax.vlines(cutoff,
               np.min(np.angle(low_pass_transfer(omega, cutoff))),
               0,
               colors='r',
               linestyles='dashed',
               label='Cutoff frequency'
               )
phase_ax.legend()

md.plot_polar(polar_ax,
              abs(low_pass_transfer(omega, cutoff)),
              np.angle(low_pass_transfer(omega, cutoff)),
              magnitude=True,
              marker='.'
              )

plt.savefig('Session_1/figures/low_pass_filter.pdf')