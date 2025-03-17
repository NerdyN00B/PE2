import numpy as np
import matplotlib.pyplot as plt
import ltspice

R = 100e3
C = 10e-6

def transfer_function(freq):
    return -1j * freq * R * C

# freq = np.logspace(1, 5, 20*4 + 1)

parser = ltspice.Ltspice('session_4/Draft1.raw')
parser.parse()

freq = parser.get_frequency()

gain = parser.get_data('V(n002)')

fig, axs = plt.subplots(2)

ax, ax2 = axs

ax.plot(freq, 20*np.log10(abs(gain)), c='k', label='Simulation')
ax.plot(freq, 20*np.log10(abs(transfer_function(freq))),
        c='r', label='Ideal')
ax.set_xscale('log')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Gain [dB]')
ax.legend()

ax2.plot(freq, np.angle(gain, deg=True), c='k', label='Simulation')
ax2.plot(freq, np.angle(transfer_function(freq), deg=True),
         c='r', label='Ideal')
ax2.set_xscale('log')
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('Phase [$^{\circ}$]')
ax2.legend()

fig.savefig('session_4/images/transfer_function.pdf')
fig.savefig('session_4/images/transfer_function.png')