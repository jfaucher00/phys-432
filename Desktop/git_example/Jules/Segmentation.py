import numpy as np
import pydicom
import matplotlib.pyplot as plt
from skimage.transform import downscale_local_mean
from DensityBinFile import write_density_file as wdf

def get_img(thick, scan_type): #For debug
    
    th_str = str(thick) + 'cm'
    path = 'Images/' + th_str + "/" + scan_type + "_" + th_str + ".dcm"
    
    ds = pydicom.dcmread(path)
    img = ds.pixel_array
    
    return img

def generate_coord(image):
    dw = 0.0067502410800385736
    #dw = 0.0065237651444548
    y, x = image.shape
    y2 = y//2 * dw
    y1 = -y2
    x1 = -dw * x
    x2 = 0.0
    
    coord_x = np.linspace(x1, x2, x+1, dtype = np.float32)
    coord_y = np.linspace(y1, y2, y+1, dtype = np.float32)
    
    return coord_x, coord_y

def cropping(real, coord_x, coord_y):
    real_ds = downscale_local_mean(real, (8,8))
    edge = np.where(real_ds>0.5*real_ds[:,0].mean(), 0, real_ds)
    proj_x = np.mean(edge, axis = 0)
    proj_y = np.mean(edge, axis = 1)
    edge_x = np.where(proj_x != 0)[0]
    edge_y = np.where(proj_y != 0)[0]
    
    crop_y = coord_y[8*edge_y[0]: 8*edge_y[-1]+1]
    crop_x = coord_x[8*edge_x[0]: 8*edge_x[-1]+1]
    
    return real[8*edge_y[0]: 8*edge_y[-1], 8*edge_x[0]: 8*edge_x[-1]], crop_x, crop_y

def material_map(image):

    material = np.zeros(image.shape, dtype = np.uint8)
    
    comb = 4
    threshold = 300*comb
    max_spect = image.max()
    
    spectrum = image.flatten()
    
    frq, val = np.histogram(spectrum, range = (0.00, max_spect), 
                            bins = max_spect//comb)
    
    check_down = (frq[:-1] > threshold) & (frq[1:] < threshold)
    edge_down = np.flatnonzero(check_down)+1
    mask = image<edge_down[-1]*comb
    material += mask
    
    return material

def density(image, material): #Need to select densities
    
    density = np.zeros(image.shape, dtype = np.float32)
    density[material == 0] = 0.001225
    density[material == 1] = 1.185
    
    return density

def complete_segmentation(image, thickness = None):
    coord_x, coord_y = generate_coord(image)
    cropped, crop_x, crop_y = cropping(image, coord_x, coord_y)
    mu_map = material_map(cropped)
    dens = density(cropped, mu_map)
    wdf(dens, 4.5, crop_x, crop_y)

# blank = get_img(4.5, "b")
real = get_img(4.5, "t")
coord_x, coord_y = generate_coord(real)
cropped, crop_x, crop_y = cropping(real, coord_x, coord_y)
mu_map = material_map(cropped)
dens = density(cropped, mu_map)
wdf(dens, 4.5, crop_x, crop_y)