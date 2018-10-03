import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
import subprocess
import shutil
    

def plot(raster, size=(5,10), aspect=1, title='', cm='gist_earth', cm_scale=(None, None)):
    """
    Plots raster images
    Args:
      raster: path or list of paths of tiffs to plot
      size: size of the plot or subplots
      aspect: aspect ratio of the plot or subplots
      title: title or list of titles for each individual plot
      cm: matplotlib colormap to use
      cm_scale: (min, max) to scale the colormap
    """
    
    # convert tiff into list
    tiffs = [raster] if not isinstance(raster, list) else raster
    titles= [title] if not isinstance(title, list) else title
    cms= [cm]*len(tiffs) if not isinstance(cm, list) else cm
    
    if not isinstance(cm_scale, list) and not isinstance(cm_scale, tuple):
        cm_scale = [(None, None)] * len(tiffs)
    elif isinstance(cm_scale, tuple):
        cm_scale = [cm_scale] * len(tiffs)
    else:
        cm_scale = cm_scale
        
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
            img = ax.imshow(data, cmap=cms[i], aspect=1)
            
            # set the color scale to match the min and max data
            if None in cm_scale[i]:
                img.set_clim(data.min(), data.max())
            else:
                img.set_clim(cm_scale[i])
            
            # turn off axes labels
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            
            if i < len(titles):
                ax.set_title(titles[i])
                
        else:
            # turn off the axis
            ax.axis('off')
        
        i += 1
