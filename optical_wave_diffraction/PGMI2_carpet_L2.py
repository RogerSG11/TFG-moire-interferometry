# Two phase-grating moire interferometer

# Carpet of intensity vs L2 (propagation distance from second grating)
# Constant grating separation

import numpy as np
import matplotlib.pyplot as plt
from optwavepckg import OptWave
from optwavepckg.utils import intensity, normalizedIntensity

# Sim parameters
N = 2e5
L = 60e-3
wvl = 1.55e-6

# Source parameters
w0 = 1.6e-3
z0 = 7.26e-3
f = -75e-3 # lens focal for cone beam

# System parameters
P = 180e-6

L0 = 11e-2
L1 = 98e-2
D = 6.5e-2

L2vals = np.linspace(0, 1, 501)

phi = np.pi/2

# Calculate field right after first grating
wave = OptWave(N,L,wvl)
wave.gaussianBeam(w0, z0=z0)
wave.angular_spectrum(L0)
wave.lens(f)
wave.angular_spectrum(L1)
wave.rectPhaseGrating(P, phi)
wave.angular_spectrum(D)
wave.rectPhaseGrating(P, phi)

# Store field 
# This allows to run the first propagation only once
x = wave.x
u = wave.U
I = []
mask = np.abs(x) <= 15e-3 # central part of image

# Test for different values of D
# Last value of D is not calculated because pcolormesh will not plot it
for L2 in L2vals:
    print(L2)
    wave.U = u
    wave.angular_spectrum(L2)
    Id = intensity(wave.U)
    
    # Take only central data
    I.append(Id[mask])


# Plot carpet
I = np.asanyarray(I)
xaux = x[mask]
plt.pcolormesh(xaux*1e3, L2vals*1e2, I, shading='nearest')
clb = plt.colorbar()
plt.xlabel('x [mm]')
plt.ylabel('L2 [cm]')
clb.set_label('Intensity [arbitrary units]')
plt.tight_layout()

plt.savefig('PGMI2_carpet-L2.png', dpi=800)

#plt.show()
