"""
Visualization of the velocity field of accelerating lava

Created on Wed Mar  9 18:37:32 2022

@author: jules faucher
@collab: mattias lazda, david tucci
"""

import numpy as np
import matplotlib.pyplot as plt

### Inputs

n = 120         # Size of the grid
steps = 30000   # Number of time steps of the simulation
dt = 9          # Size of the time step
dx = 1          # Size of a grid element
D = 0.1         # Diffusioon constant
g = 0.01        # Gravitationnal acceleration
alpha = 10      # Angle of the slope in degrees

### Important scalars

B = D*dt/dx**2               # B <= 1 to respect courant condition
angle = 10/180*np.pi         # Conversion of alpha in radians
x = np.arange(0, n, dx)      # Creating the grid's scale
a = g*np.sin(angle)          # Acceleration of the lava
y = -a/D*(0.5*x*x - x[-1]*x) # Analytical result for steady-state
A = (1 + 2*B)*np.eye(n) - B*np.eye(n, k = 1) - B*np.eye(n, k = -1) # Creating A

#Boundary conditions
A[0] = np.zeros(n)  # Ensures that the velocity at the ground is 0
A[0][0] = 1
A[-1][-1] = 1 + B   # Ensures that there is no strain at the lava's surface

f = np.zeros(n)     # Creates the velocity field, initially at 0

### Plot definitions 

plt.ion()
fig, ax = plt.subplots(1,1)
ax.plot(x, y, "--", color = "black")    # Plot the analytical soln
plt_obj, = ax.plot(x, f, color = "red") # Plot the initial field

fig.canvas.draw() 

### Main loop

for t in range(steps):
    
    f = np.linalg.solve(A, f) # Solve the system
    
    f[1:] += a*dt # Acceleration acting on the system
    
    if t%200 == 0: # Plotting only one frame out of 500 to decrease cpu runtime
        plt_obj.set_ydata(f)
        ax.set_title('t = ' + str(t*dt))
        fig.canvas.draw()
        plt.pause(0.001)