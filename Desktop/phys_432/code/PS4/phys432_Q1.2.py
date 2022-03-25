# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 21:44:04 2022

@author: jules
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as cf

### Question 2 ###

def cost(m, u):
    B = m/0.035 # Bird number
    return 2.3e-4*B**(-1/3)*u*u + 2.53*B**(1/3)/(u*u) + 10.7*B**(-0.25)/u

u = np.logspace(-1, 3, 500)
m = np.logspace(-2, 2, 5)
lm = len(m)

data = np.zeros((lm, len(u)))

for i in range(lm):
    data[i] = cost(m[i], u)
    
if True:
    
    for i in range(lm):
        d = data[i]
        plt.loglog(u, d, label = "{}kg".format(m[i]))
        # plt.loglog(u[d.argmin()], np.amin(d), "o")
    plt.legend()
    plt.xlabel("Speed [m/s]", fontsize = 14)
    plt.ylabel(r"$\varepsilon$", fontsize = 14)
    plt.title(r"$\varepsilon$ as a Function of Speed", fontsize = 16)
    plt.grid()
    plt.show()


### Question 3 ###

mins = np.amin(data, axis = 1)

m_plot = np.logspace(-2, 2)

def pwr_law(x, A, B):
    return A*x**B

pars, cov = cf(pwr_law, m, mins)
expect = pwr_law(m_plot, pars[0], pars[1])

plt.loglog(m_plot, expect, "--", label = "Expectation")
plt.loglog(m, mins, "o", label = "Data")
plt.ylim(top = 1)
plt.legend()
plt.xlabel("Mass of the Bird [kg]", fontsize = 14)
plt.ylabel(r"$\varepsilon_{min}$", fontsize = 14)
plt.title(r"$\varepsilon_{min}$ as a Function of Mass", fontsize = 16)
plt.text(0.01, 0.1, "pwr = {A}({B})".format(A = round(pars[1], 3), B = int(1000*np.sqrt(cov[1][1]))))
plt.grid()
plt.show()









