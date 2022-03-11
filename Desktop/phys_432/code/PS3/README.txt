Author: Jules Faucher
Collaborators: Mattias Lazda, David Tucci

This script simulates the velocity field of lava flowing down a slope of angle alpha.

The simulation uses a diffusion algorithm with boundary conditions such that there is no slip at the lava-ground interface,
and that there is no strain at the surface of the lava. Moreover, at every step of the simulation, elements of the grid are
accelerated given the gravitationnal acceleration and the angle of the slope.