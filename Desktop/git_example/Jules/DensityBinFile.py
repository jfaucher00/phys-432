from sys import byteorder
import numpy as np

def write_density_file(density, thickness, x, y):
    
    densityMatrix = density.T

    with open('C:/Users/jules/Desktop/density_file.bin', 'wb') as file:
        
        #1st entry, Big or Little Endian
        if(byteorder=="little"):
            file.write((1).to_bytes(1, byteorder=byteorder, signed=False))
        else:
            file.write((0).to_bytes(1, byteorder=byteorder, signed=False))
        
        #2nd entries, numOfRegions, 32 bit integers
        Nx, Ny = densityMatrix.shape
        Nz = 1
        
        #32 bits = 4 bytes
        file.write(Nx.to_bytes(4, byteorder=byteorder, signed=False))
        file.write(Ny.to_bytes(4, byteorder=byteorder, signed=False))
        file.write(Nz.to_bytes(4, byteorder=byteorder, signed=False))
        
        #3rd entries, plane positions, 32 bit floats in increasing order
        z = np.linspace(52.6035-thickness, 52.6035, Nz+1, dtype = np.float32)
        
        x.tofile(file)
        y.tofile(file)
        z.tofile(file)
        
        #4th entries, mass densities, 32 bit floats
        massDensities = densityMatrix.flatten("F")
        massDensities.tofile(file)