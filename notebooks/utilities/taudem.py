import os
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
import subprocess

def plot_tiff(tiff, size=(5,5), aspect=1):
    # change the aspect ration to stretch or compress the image
    
    # read the tiff using the gdal library  
    ds = gdal.Open(tiff)
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray()

    # set all negative values (i.e. nodata) to zero so that the map is displayed properly
    data[data<0] = 0

    # create figure to hold plot (figsize=(width, height))
    plt.figure(figsize=size)

    # plot the DEM and display the results
    plt.imshow(data, cmap='gist_earth', aspect=aspect)
    plt.show()
    
    
    
def run_cmd(cmd, processors=1):
    
    # build the mpi command
    command = 'mpiexec -n %d %s' % (processors, cmd)
        
    # execute the process
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    
    # Grab stdout line by line as it becomes available.  This will loop until p terminates.
    while p.poll() is None:
        l = p.stdout.readline() # This blocks until it receives a newline.
        print(l.strip().decode('utf-8'))
        
    # When the subprocess terminates there might be unconsumed output 
    # that still needs to be processed.
    print(p.stdout.read().strip().decode('utf-8'))