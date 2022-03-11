"""
Created on Thu Mar 10 17:32:41 2022

@author: jules
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

### Problem 2.2

rho = 1  #
R = 15    #
L = 170    #
c_f = 1     #
c_d = 0.3   #
nu_water = 0.01
nu = np.linspace(1, 1e4, 5000)*nu_water

u = []

for i in nu:
    P = lambda u : 0.5*np.pi*rho*u*u*R*((2*L*100*i + R*c_d)*u + 6*i) - 8.11e9
    u += [fsolve(P, 0.5)[0]]
    
u = np.array(u)
plt.semilogx(nu, u, label = "Swimmer")
plt.title("Velocity as a Function of Viscosity at Constant Power", fontsize = 16)
plt.xlabel("Viscosity of the Fluid [cm^2/s]", fontsize = 14)
plt.ylabel("Velocity [cm/s]", fontsize = 14)
plt.axvline(0.83, label = "Soap", color = "red")
plt.axvline(5.00, label = "Wax", color = "orange")
plt.axvline(30.00, label = "Shampoo", color = "green")
plt.axvline(9.50, label = "glycerine", color = "black")
plt.grid()
plt.legend()

plt.show()

### Problem 2.3

oly_t = np.array([47.58, 47.80, 47.85, 47.88, 48.01, 48.02, 48.12, 48.41])
oly_v = 1e4/oly_t/2 # Find velocity
oly_err = np.mean((oly_v[0] - oly_v[1:]))

rec_err = 25

plt.semilogx(nu, (100 - u))
plt.title("Velocity Difference as a Function of Velocity", fontsize = 16)
plt.xlabel("Viscosity of the Fluid [cm^2/s]", fontsize = 14)
plt.ylabel("Velocity difference [%]", fontsize = 14)
plt.axhline(oly_err, label = "Olympic Margin", color = "red")
plt.axhline(-oly_err, color = "red")
plt.axhline(75 + 10, label = "Recr. Margin", color = "green")
plt.axhline(75 - 10, color = "green")
plt.grid()
plt.legend()
plt.show()

