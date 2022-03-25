"""
Created on Sat Mar 19 10:18:03 2022

@author: Jules Faucher
@collaborators: Mattias Lazda, David Tucci, Nicolas Desjardins

Simulates an adiabatic shock using a donor cell advection method.
"""

import numpy as np
import matplotlib.pyplot as pl

Ngrid = 100     # Size of the grid
Nsteps = 5000   # Numbers of time steps
dt = 0.012      # Duration of time step
dx = 1.5        # Size of cell
gamma = 5/3     # Heat capacity ratio
g_ratio = (gamma - 1)/gamma # Quantity used often

x = np.arange(Ngrid) * dx # grid
f1 = np.ones(Ngrid)       # rho
f2 = np.zeros(Ngrid)      # rho * u
f3 = np.ones(Ngrid)       # rho * e_tot
u = np.zeros(Ngrid+1)     # advective velocity (keep the 1st and last element zero)
P = g_ratio*(f3 - 0.5*f2*f2/f1) # Pressure at every cell
cs2 = gamma*P/f1          # Speed of sound at each cell
u_wave = f2/f1            # Speed of the wave per cell
mach = u_wave/cs2**0.5    # Mach number at each cell

def advection(f, u, dt, dx): #Advection function from example posted on mycourses
    # calculating flux terms
    J = np.zeros(len(f)+1) # keeping the first and the last term zero
    J[1:-1] = np.where(u[1:-1] > 0, f[:-1] * u[1:-1], f[1:] * u[1:-1])
    f = f - (dt / dx) * (J[1:] - J[:-1]) #update

    return f

# Apply initial Gaussian perturbation
Amp, sigma = 1e4, Ngrid/10
f3 += Amp*np.exp(-(x - x.max()/2)**2/sigma**2)

# plotting
pl.ion()
fig, ax = pl.subplots(2,1)

x1, = ax[0].plot(x, f1, ".", color = "blue")
ax[0].axhline(4, color = "black", label = "Expected density")
ax[0].set_xlim([0, dx*(Ngrid - 1)])
ax[0].set_ylim([0, 5])
ax[0].set_xlabel('x')
ax[0].set_ylabel('Density')
ax[0].legend()

x2, = ax[1].plot(x, mach, ".", color = "red")
ax[1].set_xlim([0, dx*(Ngrid - 1)])
ax[1].set_ylim([-2, 2])
ax[1].set_xlabel('x')
ax[1].set_ylabel('Mach Number')

fig.canvas.draw()

for ct in range(Nsteps):
    # advection velocity at the cell interface
    u[1:-1] = 0.5 * ((f2[:-1] / f1[:-1]) + (f2[1:] / f1[1:]))

    
    f1 = advection(f1, u, dt, dx)   # Advect density
    f2 = advection(f2, u, dt, dx)   # Advect momentum

    P = g_ratio * (f3 - 0.5*f2*f2/f1)   # Update pressure
    cs2 = gamma*P/f1                    # Update speed of sound
    
    f2[1:-1] -= 0.5*dt/dx*(P[2:] - P[:-2])  # Update momentum
    f2[0] -= 0.5*dt/dx*(P[1] - P[0])        # Enforce B.C.
    f2[-1] -= 0.5*dt/dx*(P[-1]-P[-2])
    
    u[1:-1] = 0.5*((f2[:-1]/f1[:-1]) + (f2[1:]/f1[1:])) # Update velocity
    
    f3 = advection(f3, u, dt, dx) # Advect energy

    P = g_ratio*(f3 - 0.5*f2*f2/f1) # Update pressure
    
    u_wave = f2/f1      # Update wave velocity
    P_wave = P*u_wave   # Power of the wave
    
    f3[1:-1] -= 0.5*dt/dx*(P_wave[2:] - P_wave[:-2])    # Update energy
    f3[0] -= 0.5*dt/dx*(P_wave[1] - P_wave[0])          # Enforce B.C.
    f3[-1] -= 0.5*dt/dx*(P_wave[-1] - P_wave[-2])
    
    P = g_ratio*(f3 - 0.5*f2*f2/f1) # Update pressure
    cs2 = gamma*P/f1                # Update speed of sound
    
    u_wave = f2/f1          # Update speed of the wave
    mach = u_wave/cs2**0.5  # Update mach number of each cell
    
    # update the plot
    x1.set_ydata(f1)
    x2.set_ydata(mach)
    fig.canvas.draw()
    pl.pause(0.001)