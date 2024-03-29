# 3PGMI - theoretical frequency and contrast of moire fringes
# Using expression from Miao 2016

import numpy as np
import matplotlib.pyplot as plt

# Setup params

wvl = 1.55e-6

P = 180e-6
f1 = f2 = f3 = 1/P

# L1 = distance from point source to first grating
L1 = 75e-3 + 32e-2
D1 = 10e-2
L = 1

'''
    Fourier series coeffs for binary phase grating
    (exponential series)
    
    Parameters:
        - n (int): order of coeff
        - phi (double): phase shift
        - f (double): duty cycle. By default 0.5.
'''
def phaseGrCoeffs(n, phi, f=0.5):
    if n == 0:
        return 1 - f + f*np.exp(-1j*phi)
    else:
        return (np.exp(-1j*phi)-1)/(n*np.pi)*np.sin(n*np.pi*f)
        

# values for D3 - D1
dvals = np.linspace(-5e-2, 5e-2, 1001)

freq = []
cont = []

for D in dvals:
    
    D3 = D + D1
    L3 = L - (L1 + D1 + D3)
    
    # fd = 1/Pd
    fd = abs(((f3-f2)*(L-L3)+(f1-f2)*L1-f2*(D1-D3))/L)
    freq.append(fd)
    
    delta1 = wvl*f1/L*(f1*L1*(D1+D3+L3) - 2*f2*L1*(D3+L3) + f3*L1*L3)
    delta2 = wvl*f2/L*(f1*L1*(D3+L3) - 2*f2*(L1+D1)*(D3+L3) + f3*(L1+D1)*L3)
    delta3 = wvl*f3/L*(f1*L1*L3 - 2*f2*(L1+D1)*L3 + f3*(L1+D1+D3)*L3)
    
    # Ambiguity functions X1 and X3
    # Only orders m=-1 and m=0 are different than 0
    X1 = 0
    X3 = 0
    for m in range(-1,1):
        Am = phaseGrCoeffs(m, np.pi/2)
        Am1 = phaseGrCoeffs(m+1, np.pi/2)
        X1 += Am1*np.conj(Am)*np.exp(-1j*2*np.pi*(m+1/2)*delta1)
        X3 += Am1*np.conj(Am)*np.exp(-1j*2*np.pi*(m+1/2)*delta3)
        
    # "Ambiguity function" X2
    # Only odd orders are different than 0
    # n in range (nmin+2, nmax+4, step=2)
    X2 = 0
    for n in range(-13, 19, 2):
        Bn = phaseGrCoeffs(n, np.pi)
        Bn2 = phaseGrCoeffs(n-2, np.pi)
        X2 += Bn2*np.conj(Bn)*np.exp(-1j*2*np.pi*(n-1)*delta2)
        
    cont.append(2*np.abs(X1)*np.abs(X2)*np.abs(X3))
    
freq = np.asarray(freq)
cont = np.asarray(cont)

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('D3-D1 [mm]')
ax1.set_ylabel('Contrast', color=color)
ax1.plot(dvals*1e3, cont, color=color)

ax2 = ax1.twinx()

color = 'tab:red'
ax2.set_ylabel('Frequency [mm^-1]', color=color)
ax2.plot(dvals*1e3, freq*1e-3, color=color)

fig.tight_layout()
plt.show()
