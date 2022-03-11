"""
Visualization of leapfrogging smoke rings

@author: Jules Faucher
@collab: Mattias Lazda, David Tucci
Created on Tue Feb  8 20:56:12 2022
"""

import numpy as np
import matplotlib.pyplot as plt

dt = 1        # Definition of the time step
Nsteps = 100  # Number of steps of the simulation

## Setting up initial conditions (vortex centres and circulation)
# Vortex rings
y_v = np.array([5.0, 5.0, -5.0, -5.0]) 
x_v = np.array([-5.0, 5.0, -5.0, 5.0])
k_v = np.array([1.0, 1.0, -1.0, -1.0])
# Setting up the plot
plt.ion()
fig, ax = plt.subplots(1 ,1)
# mark the initial positions of vortices
p, = ax.plot(x_v, y_v, "k+", markersize = 10)
# play around with the marker size and type as you see fit
# draw the initial velocity streamline
# Set the boundaries of the plot and grid
x_left = -10
x_right= 30
y_top = 10
y_bot = -10
Y, X = np.mgrid[y_bot: y_top: 360j, x_left: x_right: 360j]
#360j sets the resolution of the cartesian grid; play around with it as you see fit
vel_x = np.zeros(np.shape(Y)) # this holds x−velocity
vel_y = np.zeros(np.shape(Y)) # this holds y−velocity
# masking radius for better visualization of the vortex centres
r_mask = 1
# with in this mask, you will not plot any streamline
# so that you can see more clearly the mouvement of the vortex centers

# This will be used to create a mask around the vortices
mask_filter = np.ones(X.shape, bool) 

for i in range(len(x_v)): #looping over each vortex
    
    dx = X - x_v[i] # Computes the distance between the center of the vortex
    dy = Y - y_v[i] # and all points on the grid in the x and y directions
    
    r2 = dx*dx + dy*dy # Compute the total distance (radius) squared
    
    vx = -k_v[i] * dy/r2 # Velocities are computed using a irrotationnal
    vy = k_v[i] * dx/r2  # vortex vector field
    
    vel_x += vx # The previously computed velocities are added to the field
    vel_y += vy
    
    mask_filter[r2 < r_mask**2] = False # We find positions on the grid where
    # r2 is greater than the mask's radius and tag them to attribute a nan value
    # in the velocity field
vel_x[mask_filter] = np.nan
    
    
# set up the boundaries of the simulation box
ax.set_xlim([x_left, x_right])
ax.set_ylim([y_bot, y_top])
# initial plot of the streamlines
ax.streamplot(X, Y, vel_x , vel_y , color = "slateblue", density = [1, 1])
# play around with density as you see fit
# see the API documentation for more details
fig.canvas.draw()
# Evolution
count = 0

while count < Nsteps:
    ## Compute advection velocity due to each vortex
    
    vx = np.zeros(len(x_v)) # Temporary arrays for advection velocities
    vy = np.zeros(len(x_v))
    
    for i in range(len(x_v)): #Looping over each vortices
        
        cur_x = x_v[i] #Current vortex being observed
        cur_y = y_v[i]
        filtre = np.ones(len(x_v), dtype = bool) #Finding the other vortices
        filtre[i] = False
        other_x = x_v[filtre] # Specifications of the three other vortices 
        other_y = y_v[filtre]
        other_k = k_v[filtre]

        dx = cur_x - other_x # Distance in x and y between the current 
        dy = cur_y - other_y # vortex and the other ones

        r2 = dx*dx + dy*dy # Total distance squared
        vx[i] = np.sum(-other_k * dy/r2)  # velocity components at the current vortex's
        vy[i] = np.sum(other_k * dx/r2)   # porition using an irrotational velocity field
        
    x_v += vx*dt #Once all velocities are computed, the positions are updated
    y_v += vy*dt
    
    
    # insert lines to re-initialize the total velocity field
    
    vel_x = np.zeros(np.shape(Y)) # this holds x−velocity
    vel_y = np.zeros(np.shape(Y)) # this holds y−velocity
    
    # This block of code is a copy of the first one
    mask_filter = np.ones(X.shape, bool)

    for i in range(len(x_v)): #looping over each vortex
        
        dx = X - x_v[i]
        dy = Y - y_v[i]
        
        r2 = dx*dx + dy*dy
        
        vx = -k_v[i] * dy/r2
        vy = k_v[i] * dx/r2
        
        vel_x += vx
        vel_y += vy
        
        mask_filter[r2 < r_mask**2] = False

    vel_x[mask_filter] = np.nan
    

    ## update plot
    # the following two lines clear out the previous streamlines
    #ax.collections = []
    #ax.patches = []

    p.set_xdata(x_v)
    p.set_ydata(y_v)
    ax.streamplot(X, Y, vel_x , vel_y , color = "slateblue", density = [1, 1])
    fig.canvas.draw()
    plt.pause(0.0005) # play around with the delay time for better visualization
    count += 1