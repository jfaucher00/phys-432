Author: Jules Faucher
Callaborators: Mattias Lazda, David Tucci

This script is used to simulate the behaviour of two leapfrogging smoke rings.

The simulation uses a superposition of velocity fields produced by irrotational flow.

Since trigometric functions are unreliable in this context, it is better to avoid using angles
to find velocities around a vortex, and use a field defined as such:

(I)    v = k*(-dy/r^2, dx/r^2)

where dx and dy are the distances in the x and y directions between two points.

The velocities at a vortex's position produced by the other vortices are added up. This net
velocity is then used to estimate the vortices' next position. This is done by using the
kinematic equation:

(II)   x(t+dt) = x(t) + v*dt

Velocity fields are found using equation I where dx and dy are the distances between a vortex and a point in space.
This is iterated over all points on the grid. The contributions of all vortices are added to produce the total field.