import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
import subprocess
import shutil

is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
    input = raw_input
else:
    import queue as queue


def get_input(text):
    return input(text)

def create_workspace(folder_name):

    # get the data directory (this is an environment variable that is provided to you)
    data_directory = os.path.join(os.environ['DATA'], folder_name)
    create_dir = True
    if os.path.exists(data_directory):
        # res = get_input('This directory already exists.\nWould you like to remove it [Y/n]? ')
        res = input('This directory already exists.\nWould you like to remove it [Y/n]? ')
        if res != 'n':
            shutil.rmtree(data_directory)
        else:
            create_dir = False
            print('Directory creation aborted')
            
    if create_dir:
        os.mkdir(data_directory)
        print('A clean directory has been created')  
    
    return data_directory
    
    
def plot_tiff(tiff, size=(5,10), aspect=1, title=''):
    """
    Plots raster images
    Args:
      tiff: path or list of paths of tiffs to plot
      size: size of the plot or subplots
      aspect: aspect ratio of the plot or subplots
      title: title or list of titles for each individual plot
    """
    
    # convert tiff into list
    tiffs = [tiff] if not isinstance(tiff, list) else tiff
    titles= [title] if not isinstance(title, list) else title
        
    # get the total number of plots
    num_plots = len(tiffs)
    
    # calculate the number of col and rows for the subplot
    num_cols = 4 if num_plots > 4 else num_plots
    num_rows = math.ceil(num_plots/4) if num_plots > 4 else 1

    # calculate the total figure width and height
    fig_width = num_cols * size[0]
    fig_height= num_rows * size[1]
    
    # create the figure and subplots
    fig, axes = plt.subplots(num_rows,num_cols,figsize=(fig_width, fig_height))
    
    # make sure axes is a list
    axes = np.array([axes]) if not isinstance(axes, list) and \
                               not isinstance(axes, np.ndarray) \
                            else axes
    # plot the data
    i = 0
    for ax in axes.reshape(-1):
        
        if i < len(tiffs):
            # get the ith dataset
            ds = gdal.Open(tiffs[i])
            band = ds.GetRasterBand(1)
            data = band.ReadAsArray()

            # set all negative values (i.e. nodata) to zero so that the map is displayed properly
            data[data<0] = 0

            # plot the data
            ax.imshow(data, cmap='gist_earth', aspect=1)
            
            # turn off axes labels
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            
            if i < len(titles):
                ax.set_title(titles[i])
                
        else:
            # turn off the axis
            ax.axis('off')
        
        i += 1
    
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