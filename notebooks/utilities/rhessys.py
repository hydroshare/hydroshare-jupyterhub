from __future__ import print_function
import urllib, json, time
import sys
import os
import errno
import zipfile
import subprocess
import logging
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
import wget
import datetime
import shutil
from IPython.core.display import display, HTML
from hydroshare import utilities 

# Plotting libraries
import math
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib
from rhessysworkflows.rhessys import RHESSysOutput
PLOT_TYPE_STD = 'standard'
PLOT_TYPE_LOGY = 'logy'
PLOT_TYPE_CDF = 'cdf'
PLOT_TYPE_SCATTER = 'scatter'
PLOT_TYPE_SCATTER_LOG = 'scatter-log'
PLOT_TYPES = [PLOT_TYPE_STD, PLOT_TYPE_LOGY, PLOT_TYPE_CDF, PLOT_TYPE_SCATTER, PLOT_TYPE_SCATTER_LOG]
PLOT_DEFAULT = PLOT_TYPE_STD

LINE_TYPE_LINE = 'line'
LINE_TYPE_DASH = 'dash'
LINE_TYPE_DASH_DOT = 'dashdot'
LINE_TYPE_COLON = 'colon'
LINE_TYPE_DOT = 'dot'
LINE_TYPE_DICT = { LINE_TYPE_LINE: '-',
                  LINE_TYPE_DASH: '--',
                  LINE_TYPE_DASH_DOT: '-.',
                  LINE_TYPE_COLON: ':',
                  LINE_TYPE_DOT: '.' }
LINE_TYPES = [LINE_TYPE_LINE, LINE_TYPE_DASH, LINE_TYPE_DASH_DOT, LINE_TYPE_COLON, LINE_TYPE_DOT]
NUM_LINE_TYPES = len(LINE_TYPES)
    
class Extent(object):

    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0

    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y


    def __repr__(self):
        return "\nmin x = " + str(self.min_x) + "\nmin y = " + str(self.min_y) + "\nmax x = " + str(self.max_x)  + "\nmax y = " + str(self.max_y) + "\n"

def plotGraph(obs, data, sizeX=1, sizeY=1, dpi=80, **kwargs):
    
    plottype = kwargs.get('plottype')
    supressObs = kwargs.get('supressObs')
    linewidth = kwargs.get('linewidth')
    linestyle = kwargs.get('linestyle')
    color = kwargs.get('color')
    column = kwargs.get('column')
    title = kwargs.get('title')
    ylabel = kwargs.get('ylabel')
    xlabel = kwargs.get('xlabel')
    legend = kwargs.get('legend')
    secondaryData = kwargs.get('secondaryData')
    secondaryColumn = kwargs.get('secondaryColumn')
    secondaryPlotType = kwargs.get('secondaryPlotType')
    
    fig = plt.figure(figsize=(sizeX, sizeY), dpi=dpi, tight_layout=True)
    ax = fig.add_subplot(111)

    if plottype == PLOT_TYPE_STD or \
       plottype == PLOT_TYPE_LOGY:
        x = obs.index
    elif plottype == PLOT_TYPE_CDF:
        x = np.linspace(min_x, max_x, num=len(obs) )
    
    # Plot observed values
    # Standard or log plot
    obs_y = obs
    if plottype == PLOT_TYPE_CDF:
        obs_ecdf = sm.distributions.ECDF(obs)
        obs_y = obs_ecdf(x)
    obs_plt = None
    if not supressObs:
        (obs_plt,) = ax.plot(x, obs_y, linewidth=2.0, color='black')
        
    # Plot modeled values 
    data_plt = []
    for (i, d) in enumerate(data):
        # Standard or log plot
        mod_y = d
        if plottype == PLOT_TYPE_CDF:
            mod_ecdf = sm.distributions.ECDF(d)
            mod_y = mod_ecdf(x)
        
        # Plot (we could move this outside of the for loop)
        if linewidth is not None:
            linewidth = linewidth[i]
        else:
            linewidth = 1.0
            
        if linestyle is not None:
            linestyle = LINE_TYPE_DICT[ linestyle[i] ]
        else:
            # Rotate styles
            styleIdx = ( (i + 1) % NUM_LINE_TYPES ) - 1
            linestyle = LINE_TYPE_DICT[ LINE_TYPES[styleIdx] ]
            
        if color:
            (mod_plt,) = ax.plot(x, mod_y, linewidth=linewidth, linestyle=linestyle,
                                 color=color[i])
        else:
            (mod_plt,) = ax.plot(x, mod_y, linewidth=linewidth, linestyle=linestyle)
        
        data_plt.append(mod_plt)
    
    # Plot annotations
    columnName = column.capitalize()
    if title:
        title = title
    else:
        if plottype == PLOT_TYPE_STD:
            title = columnName
        elif plottype == PLOT_TYPE_LOGY:
            title = "log(%s)" % (columnName,)
        elif plottype == PLOT_TYPE_CDF:
            title = "Cummulative distribution - %s" % (columnName,) 
    fig.suptitle(title, y=0.99)

    # X-axis
    if plottype == PLOT_TYPE_STD or \
       plottype == PLOT_TYPE_LOGY:
        num_years = len(x) / 365
        if num_years > 4:
            if num_years > 10:
                ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
            else:
                ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator(interval=3))
        else:
            ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%b-%Y'))
        # Rotate
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=45)
        plt.setp( ax.xaxis.get_majorticklabels(), fontsize='x-small')
    
    if plottype == PLOT_TYPE_CDF:
        ax.set_xlim(min_x, max_x)
        ax.set_xscale('log')
        if xlabel:
            ax.set_xlabel(xlabel)
        else:
            ax.set_xlabel( columnName )
    elif xlabel:
        ax.set_xlabel(xlabel)
    
    # Y-axis
    if plottype == PLOT_TYPE_LOGY:
        ax.set_yscale('log')
    
    if ylabel:
        ax.set_ylabel(ylabel)
    elif plottype != PLOT_TYPE_CDF:
        y_label = columnName
        if plottype == PLOT_TYPE_LOGY:
            y_label = "log( %s )" % (columnName,)
        ax.set_ylabel( y_label )
    
    if supressObs:
        legend_items = legend
    else:
        data_plt.insert(0, obs_plt)
        legend_items = ['Observed'] + legend
    
    # Plot secondary data (if specified)
    if secondaryData and \
       (plottype == PLOT_TYPE_STD or plottype == PLOT_TYPE_LOGY):
        sec_file = open(secondaryData, 'r')
        (sec_datetime, sec_data) = RHESSysOutput.readColumnFromFile(sec_file,
                                                                    secondaryColumn,
                                                                    startHour=0)
        sec_file.close()
        sec = pd.Series(sec_data, index=sec_datetime)
        # Align timeseries
        (sec_align, obs_align) = sec.align(obs, join='inner')
        # Plot
        ax2 = ax.twinx()
        if secondaryPlotType == 'line':
            (sec_plot,) = ax2.plot(x, sec_align)
        elif secondaryPlotType == 'bar':
            sec_plot = ax2.bar(x, sec_align, facecolor='blue', edgecolor='none', width=2.0)
        secondaryLabel = secondaryColumn.capitalize()
        if secondaryLabel:
            secondaryLabel = secondaryLabel
        ax2.invert_yaxis()
        ax2.set_ylabel(secondaryLabel)
    #ax.set_zorder(ax2.get_zorder()+1) # put ax in front of ax2
    #ax.patch.set_visible(False) # hide the 'canvas' 
    
    # Plot legend last
    num_cols = len(data)
    if not supressObs:
        num_cols += 1
    
    if plottype == PLOT_TYPE_CDF:
        fig.legend( data_plt, legend_items, 'lower center', fontsize='x-small', 
                    bbox_to_anchor=(0.5, -0.015), ncol=num_cols, frameon=False )
    else:
        fig.legend( data_plt, legend_items, 'lower center', fontsize='x-small', 
                    bbox_to_anchor=(0.5, -0.01), ncol=num_cols, frameon=False )

def plot_rhessys_results(outfileSuffix,
        obs,
        column,
        legend,
        plottype=PLOT_DEFAULT,
        data=None, 
        behavioralData=None,
        color=[None],
        linewidth=None,
        linestyle=None,
        title=None,
        x=None,
        y=None,
        titlefontsize=12,
        scatterwidth=1,
        fontweight='regular',
        legendfontsize=6,
        axesfontsize=12,
        ticklabelfontsize=12,
        figureX=4,
        figureY=3,
        supressObs=False,
        secondaryData=None,
        secondaryPlotType='bar',
        secondaryColumn=None,
        secondaryLabel=None
       ):
    """
    plottype: Type of plot
    outfileSuffix: Suffix to append on to name part of file name
    obs: File containing observed data, required=True
    data: One or more RHESSys output data files
    behavioralData: One or more ensemble output files from RHESSys behavioral runs
    color: Color of symbol to be applied to plots of data. Color must be expressed in form recognized by matplotlib
    linewidth: Width of lines to be applied to plots of data. Value must be float in units of points
    linestyle: Style of symbol to be applied to plots of data. Styles correspond to those of matplotlib
    column: Name of column to use from data files
    title: Title of figure
    legend: Legend item labels
    x: X-axis label
    y: Y-axis label
    titlefontsize
    scatterwidth: Width to use for lines and markers in scatter plots.  
                  Markers size will be determine by multiplying scatterwidth by 6
    fontweight: 
    legendfontsize: 
    axesfontsize:
    ticklabelfontsize: 
    figureX: The width of the plot, in inches
    figureY: The height of the plot, in inches
    supressObs: Do not plot observed data.  Observed data will still be used for aligning timeseries. 
                Not applicable to scatter plot output
    secondaryData: A data file containing the varaible to plot on a secondary Y-axis
    secondaryPlotTyp: Type of plot to use for secondary data.
    secondaryColumn: Name of column to use from secondary data file
    secondaryLabel: Label to use for seconary Y-axis
    """
    
    
    if color:
        if len(color) != len(data):
            return 'Number of colors must match number of data files'
    
    if linewidth:
        if min(linewidth) <= 0.0:
            return 'All line widths must be > 0.0'
        if len(linewidth) != len(data):
            return 'Number of line widths must match number of data files'
            
    if linestyle:
        if len(linestyle) != len(data):
            return 'Number of line styles must match number of data files'
    
    if secondaryData and not secondaryColumn:
        return 'A secondary data file was specified, but the secondary column to use was not'
    
    if data and ( len(data) != len(legend) ):
        return 'Number of legend items must equal the number of data files'
    elif behavioralData and ( len(behavioralData) != len(legend) ):
        return 'Number of legend items must equal the number of data files'

    # Open data and align to observed
    obs_align = None
    data_list = []
    max_x = min_x = 0
    
    if data:
        # Open observed data
        obs_file = open(obs, 'r')
        (obs_datetime, obs_data) = RHESSysOutput.readObservedDataFromFile(obs_file,
                                                                          readHour=False)
        obs_file.close()
        obs = pd.Series(obs_data, index=obs_datetime)
        
        for d in data:
            mod_file = open(d, 'r')
            (tmp_datetime, tmp_data) = RHESSysOutput.readColumnFromFile(mod_file, column, startHour=0)
            tmp_mod = pd.Series(tmp_data, index=tmp_datetime)
            # Align timeseries
            (mod_align, obs_align) = tmp_mod.align(obs, join='inner')
            tmp_max_x = max(mod_align.max(), obs_align.max())
            if tmp_max_x > max_x:
                max_x = tmp_max_x
            min_x = max(min_x, mod_align.min())
        
            mod_file.close()
            data_list.append( mod_align )
    elif behavioralData:
        
        # Open observed data (behavioral data has hour in it, so we need to read obs. data differently)
        obs_file = open(obs, 'r')
        (obs_datetime, obs_data) = RHESSysOutput.readObservedDataFromFile(obs_file,
                                                                          readHour=True)
        obs_file.close()
        obs = pd.Series(obs_data, index=obs_datetime)
        
        for b in behavioralData:
            tmp_mod = pd.read_csv(b, index_col=0, parse_dates=True)
            # Convert df to series
            tmp_mod = pd.Series(tmp_mod[column], index=tmp_mod.index)
            # Align timeseries
            (mod_align, obs_align) = tmp_mod.align(obs, join='inner')
            tmp_max_x = max(mod_align.max(), obs_align.max())
            if tmp_max_x > max_x:
                max_x = tmp_max_x
            min_x = max(min_x, mod_align.min())
        
            data_list.append( mod_align )

    kwargs = dict(legend=legend,
                 column=column,
                 plottype=plottype,
                 behavioralData=behavioralData,
                 color=color,
                 linewidth=linewidth,
                 linestyle=linestyle,
                 title=title,
                 xlabel=x,
                 ylabel=y,
                 titlefontsize=titlefontsize,
                 scatterwidth=scatterwidth,
                 fontweight=fontweight,
                 legendfontsize=legendfontsize,
                 axesfontsize=axesfontsize,
                 ticklabelfontsize=ticklabelfontsize,
                 figureX=figureX,
                 figureY=figureY,
                 supressObs=supressObs,
                 secondaryData=secondaryData,
                 secondaryPlotType=secondaryPlotType,
                 secondaryColumn=secondaryColumn,
                 secondaryLabel=secondaryLabel)
    
    if plottype == PLOT_TYPE_SCATTER:
        print('%s: not supported at this time' % PLOT_TYPE_SCATTER)
        return
        
    elif plottype == PLOT_TYPE_SCATTER_LOG:
        print('%s: not supported at this time' % PLOT_TYPE_SCATTER_LOG)
        return
    else:
        plotGraph(obs_align, data_list, 
                  sizeX=figureX, sizeY=figureY,
                 **kwargs)
    # Output plot
    filename = plottype
    if outfileSuffix:
        filename += '_' + outfileSuffix
    plot_filename_png = "%s.png" % (filename,)
    plot_filename_pdf = "%s.pdf" % (filename,)
    plt.savefig(plot_filename_png)
    plt.savefig(plot_filename_pdf)

class RHESSysWorkflow(object):
 

    ######################################
    ## Important variables for catchment(s)
    extent = Extent(0,0,0,0)
    
    ######################################
    ## Common variables for RHESSysWorkflow
    project_location = '/tmp'
    project_name = 'test'
    output_folder_location = project_location + "/" + project_name
    sub_project_folder = ''
    gageid = '01589312'
    publisher = 'Brian Miles <brian_miles@unc.edu>'
    
    lai_fullpathname_with_ext = ''
    climate_data_fullpathname =''
    station_data_fullpathname = ''
    dem_cell_threshold = 500
    areaEstimate = 1.5
    rhessys_source_location = ''
    model_start_year = 2000
    model_start_month = 1
    model_start_day = 1
    model_end_year = 2001
    model_end_month = 1
    model_end_day = 1


    ######################################
    ## Common variables for HydroTerre Workflows
    ht_start_date = '2000-01-01'
    ht_end_date = '2001-01-01'
    huc_list_as_string = 'NONE'
    huc_list_count = 0
    huc_list = []

    ######################################
    ## Variables for this tool
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    timespan = end_time - start_time
    logger = ''
    hdlr = ''

    ###############################################################################################
    def __init__(self, project_location=os.environ['DATA'], 
                 project_name='test_project', 
                 gageid='01589312', 
                 start_date='2008-01-01', 
                 end_date='2010-01-01', 
                 rhessys_source_location='', 
                 publisher='RHESSysWorkflow'):
        
        #project_location = os.environ['DATA'] if project_location is None else project_location
        self.project_location = project_location
        self.project_name = project_name
        self.gageid = gageid
        self.ht_start_date = start_date
        self.ht_end_date = end_date
        self.output_folder_location = self.project_location + "/" + self.project_name
        self.sub_project_folder = self.output_folder_location + "/" + self.project_name
        self.rhessys_source_location = rhessys_source_location
        self.publisher = publisher
        self.filter_times()

        ######################################
        ## Create project location
        if os.path.exists(self.output_folder_location):
            res = raw_input('Project [%s] already exists, would you like to remove it [Y/n]? ' % self.project_name)
            if res != 'n':
                print('Creating a clean directory for project [{0}]'.format(self.project_name))
                shutil.rmtree(self.output_folder_location)
        self.create_path(self.output_folder_location)
        self.create_path(self.sub_project_folder)
        self.setup_log()
        
        rp = utilities.get_relative_path(self.output_folder_location)
        up = utilities.get_server_url_for_path(self.output_folder_location)
        display(HTML('<pre>RHESSys project has been initialized at:<br>' +
                     '<a href={0} target="_blank">{1}<a></pre>'.format(up, rp)))
        
        ######################################
        ## Create workflow
        #print("Start Executing workflow")
        #self.execute_workflow()
        #print("End Executing workflow")

        # prepare grass environment extensions
        if not os.path.exists(os.path.join(os.environ['HOME'], '.grass7')):
            print('Preparing grass7 installation... ', end='')
            try:
                prepare_script = os.path.join(os.path.dirname(__file__), 'prepare_grass.sh')
                my_command = 'sh %s jupyter' % prepare_script
                self.logger.info(my_command)
                output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
                print('done')
            except Exception as e:
                self.logger.error(str(e))
                
            
            

    ###############################################################################################
    ### Common functions to manage workflow
    def create_path(self, path):
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST or not os.path.isdir(path):
                raise


    def setup_log(self):
        log_file = self.output_folder_location + "/" + self.project_name + ".log"
        print('Log file location: ' + log_file)
        self.logger = logging.getLogger("myApp")
        self.hdlr = logging.FileHandler(log_file)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)
 

    def unzip_etv_zip_file_at_path(self, input_location, etv_output_folder_location):
        try:
            zfile = zipfile.ZipFile(input_location)
            zfile.extractall(etv_output_folder_location)
            zfile.close()
        except Exception as e:
            print(str(e))



    ###############################################################################################
    ### Functions to retrieve properties from RHESSysWorkflow

    def filter_times(self):
        start_split = self.ht_start_date.split('-')
        end_split = self.ht_end_date.split('-')

        self.model_start_year = int(start_split[0])
        self.model_start_month = int(start_split[1])
        self.model_start_day = int(start_split[2])
        self.model_end_year = int(end_split[0])
        self.model_end_month = int(end_split[1])
        self.model_end_day = int(end_split[2])

    def get_Metadata_filename(self):
        return self.project_location + "/" + self.project_name + "/" + self.project_name + "/metadata.txt"

    def get_Extent_from_RHESSysWorkflows_Metadata_File(self):

        try:
            metadata_file_and_path = self.get_Metadata_filename()       
            self.logger.info(metadata_file_and_path)

            extent_min_x = ''
            extent_max_x = ''
            extent_min_y = ''
            extent_max_y = ''

            f = open(metadata_file_and_path, 'r')
            lines = f.readlines()
            for line in lines:
                #print line
                fnd = line.find('bbox_wgs84 = ')
                if fnd == 0:
                    #print line
                    split1 = line.split(' = ') #BEWARE OF SPACES
                    split2 = split1[1].replace('\n','').split(' ')
                    #print split2
                    extent_min_x = split2[0]
                    extent_min_y = split2[1]
                    extent_max_x = split2[2]
                    extent_max_y = split2[3]


            result = Extent(extent_min_x,extent_min_y,extent_max_x,extent_max_y)
            self.logger.info(result)
            return result
        except Exception as e:
            self.logger.info("FAILED->get_Extent_from_RHESSysWorkflows_Metadata_File")
            self.logger.error(str(e))
            return -1101


    ###############################################################################################
    ### Functions to execute RHESSysWorkflow
    def RegisterDEMOptions(self, options):
        try:
            my_command = "RegisterDEM.py " + options
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->RegisterDEMOptions")
            self.logger.error(str(e))
            return -1102
        
    def RegisterDEM(self, sub_project_folder, dem_file):
        try:
            my_command = "RegisterDEM.py -p " + sub_project_folder + " -d " + dem_file
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->RegisterDEM")
            self.logger.error(str(e))
            return -1103
        
    def RegisterGage(self, sub_project_folder, gage_file, layername, id_attribute, id_value):
        try:
            my_command = "RegisterGage.py -p " + sub_project_folder + " -g " + gage_file + " -l " + layername + " -a " + id_attribute + " -d " + id_value
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->RegisterGage")
            self.logger.error(str(e))
            return -1104

    def RegisterRasterOptions(self, options):
        try:
            my_command = "RegisterRaster.py " + options
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->RegisterRasterOptions")
            self.logger.error(str(e))
            return -1105
         
    def RegisterRaster(self, sub_project_folder, raster_type, raster_file):
        try:
            my_command = "RegisterRaster.py -p " + sub_project_folder + " -t " + raster_type + " -r " + raster_file
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->RegisterRaster")
            self.logger.error(str(e))
            return -1106
        
    def get_NHDStreamflowGageIdentifiersAndLocation(self, sub_project_folder, gageid):
        try:
            my_command = "GetNHDStreamflowGageIdentifiersAndLocation.py -p " + sub_project_folder + " -g " + gageid
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->get_NHDStreamflowGageIdentifiersAndLocation")
            self.logger.error(str(e))
            return -1107

    def get_CatchmentShapefileForNHDStreamflowGage(self, sub_project_folder):
        try:
            my_command = "GetCatchmentShapefileForNHDStreamflowGage.py --overwrite -p " + sub_project_folder
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->get_CatchmentShapefileForNHDStreamflowGage")
            self.logger.error(str(e))
            return -1108

    def get_BoundingboxFromStudyareaShapefile(self, sub_project_folder):
        try:
            my_command = "GetBoundingboxFromStudyareaShapefile.py -p " + sub_project_folder
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except subprocess.CalledProcessError as e:
            self.logger.info("FAILED->get_BoundingboxFromStudyareaShapefile")
            self.logger.error(str(e))
            return -1109
        except Exception as e:
            self.logger.info("FAILED->get_BoundingboxFromStudyareaShapefile")
            self.logger.error(str(e))
            return -1110

    def get_USGSDEMForBoundingbox(self, sub_project_folder):
        try:
            my_command = "GetUSGSDEMForBoundingbox.py --overwrite -p " + sub_project_folder
            self.logger.info(my_command)

            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->get_USGSDEMForBoundingbox")
            self.logger.error(str(e))
            return -1111

    def get_USGSNLCDForDEMExtent(self, sub_project_folder):
        try:
            my_command = "GetUSGSNLCDForDEMExtent.py -p " + sub_project_folder
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->get_USGSNLCDForDEMExtent")
            self.logger.error(str(e))
            return -1112

    def get_SSURGOFeaturesForBoundingbox(self, sub_project_folder):
        try:
            my_command = "GetSSURGOFeaturesForBoundingbox.py -p " + sub_project_folder
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->get_SSURGOFeaturesForBoundingbox")
            self.logger.error(str(e))
            return -1113

    def GenerateSoilPropertyRastersFromSSURGO(self, sub_project_folder):
        try:
            my_command = "GenerateSoilPropertyRastersFromSSURGO.py -p " + sub_project_folder
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->GenerateSoilPropertyRastersFromSSURGO")
            self.logger.error(str(e))
            return -1114


    def Register_LAI_Raster(self, sub_project_folder, lai_fullpathname_with_ext, publisher):
        try:
            my_command = "RegisterRaster.py -p " + sub_project_folder + " -t lai -r " + lai_fullpathname_with_ext + " -b \"" + publisher + "\" --force "
            self.logger.info(my_command) 
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->Register_LAI_Raster")
            self.logger.error(str(e))
            return -1115


    def CreateGRASSLocationFromDEM(self, sub_project_folder, description):
        try:
            my_command = "CreateGRASSLocationFromDEM.py -p " + sub_project_folder + " -d " + description
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->CreateGRASSLocationFromDEM")
            self.logger.error(str(e))
            return -1116


    def ImportRHESSysSource(self, sub_project_folder, source_code_location=None):
        try:
            if source_code_location is not None:
                my_command = "ImportRHESSysSource.py --overwrite -p " + sub_project_folder + " -s " + source_code_location
            else:
                my_command = "ImportRHESSysSource.py --overwrite -p " + sub_project_folder
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->ImportRHESSysSource")
            self.logger.error(str(e))
            return -1117


    def ImportClimateData(self, sub_project_folder, climate_data_location):
        try:
            my_command = "ImportClimateData.py -p " + sub_project_folder + " -s " + climate_data_location
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->ImportClimateData")
            self.logger.error(str(e))
            return -1118


    def GenerateBaseStationMap(self, sub_project_folder, station_data_location):
        try:
            my_command = "GenerateBaseStationMap.py -p " + sub_project_folder + " -b " + station_data_location
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->GenerateBaseStationMap")
            self.logger.error(str(e))
            return -1119


##TODO OTHER VARIABLES
    def DelineateWatershed(self, sub_project_folder, dem_cell_threshold, areaEstimate):
        try:
            my_command = "DelineateWatershed.py -p " + sub_project_folder + " -t " + str(dem_cell_threshold) + " -a " + str(areaEstimate)
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->DelineateWatershed")
            self.logger.error(str(e))
            return -1120

    def GeneratePatchMapOptions(self, options):
        try:
            my_command = "GeneratePatchMap.py " + options
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->GeneratePatchMapOptions")
            self.logger.error(str(e))
            return -1121

##TODO OTHER VARIABLES
    def GeneratePatchMap(self, sub_project_folder):
        try:
            my_command = "GeneratePatchMap.py -p " + sub_project_folder + " -t clump -c elevation"
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->GeneratePatchMap")
            self.logger.error(str(e))
            return -1122

    def GenerateSoilTextureMap(self, sub_project_folder, options=''):
        try:
            my_command = "GenerateSoilTextureMap.py %s -p %s" %(options, sub_project_folder)
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->GenerateSoilTextureMap")
            self.logger.error(str(e))
            return -1123

    def ImportRasterMapIntoGRASS(self, sub_project_folder, texture, mode):
        try:
            my_command = "ImportRasterMapIntoGRASS.py -p " + sub_project_folder + " -t " + texture + " -m " + mode
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->ImportRasterMapIntoGRASS")
            self.logger.error(str(e))
            return -1124

    def ImportRasterMapIntoGRASS_LAI(self, sub_project_folder):
        try:
            my_command = "ImportRasterMapIntoGRASS.py -p " + sub_project_folder + " -t lai -m nearest"
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->ImportRasterMapIntoGRASS_LAI")
            self.logger.error(str(e))
            return -1125

    def ImportRasterMapIntoGRASS_LANDCOVER(self, sub_project_folder):
        try:
            my_command = "ImportRasterMapIntoGRASS.py -p " + sub_project_folder + " -t landcover -m nearest"
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->ImportRasterMapIntoGRASS_LANDCOVER")
            self.logger.error(str(e))
            return -1126
        
    def RegisterLandcoverReclassRulesOptions(self, options):
        try:
            my_command = "RegisterLandcoverReclassRules.py " + options
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->RegisterLandcoverReclassRulesOptions")
            self.logger.error(str(e))
            return -1127

    def RegisterLandcoverReclassRules(self, sub_project_folder):
        try:
            my_command = "RegisterLandcoverReclassRules.py -p " + sub_project_folder + " -k"
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->RegisterLandcoverReclassRules")
            self.logger.error(str(e))
            return -1128
        
    def GenerateLandcoverMapsOptions(self, options):
        try:
            my_command = "GenerateLandcoverMaps.py " + options
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->GenerateLandcoverMapsOptions")
            self.logger.error(str(e))
            return -1129

    def GenerateLandcoverMaps(self, sub_project_folder):
        try:
            my_command = "GenerateLandcoverMaps.py -p " + sub_project_folder
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->GenerateLandcoverMaps")
            self.logger.error(str(e))
            return -1130

    def GenerateWorldTemplateOptions(self, options):
        try:
            my_command = "GenerateWorldTemplate.py " + options
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->GenerateWorldTemplateOptions")
            self.logger.error(str(e))
            return -1131
        
#TODO NAME OF CLIMATE STATION
    def GenerateWorldTemplate(self, sub_project_folder):
        try:
            my_command = "GenerateWorldTemplate.py -p " + sub_project_folder + " -c HT_RHESSys"
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->GenerateWorldTemplate")
            self.logger.error(str(e))
            return -1132

    def CreateWorldfile(self, sub_project_folder):
        try:
            my_command = "CreateWorldfile.py -p " + sub_project_folder + " -v"
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->CreateWorldfile")
            self.logger.error(str(e))
            return -1133

    def CreateFlowtableOptions(self, options):
        try:
            my_command = "CreateFlowtable.py " + options
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->CreateFlowtableOptions")
            self.logger.error(str(e))
            return -1134
        
    def CreateFlowtable(self, sub_project_folder):
        try:
            my_command = "CreateFlowtable.py -p " + sub_project_folder + " --routeRoads"
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->CreateFlowtable")
            self.logger.error(str(e))
            return -1135

    def RunLAIRead(self, sub_project_folder):
        try:
            my_command = "RunLAIRead.py -p " + sub_project_folder + " -v"
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->RunLAIRead")
            self.logger.error(str(e))
            return -1136

    def RunCmdOptions(self, options):
        try:
            
            my_command = "RunCmd.py " + options

            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->RunCmdOptions")
            self.logger.error(str(e))
            return -1137
        
    ##TODO MORE OPTIONS
    def RunCmd(self, sub_project_folder, addmonths):
        try:
            output_location = sub_project_folder + "/rhessys/tecfiles/tec_daily.txt"
            my_command = "RunCmd.py -p " + sub_project_folder + ' echo "2008 10 1 1 print_daily_on" > ' + output_location
            #my_command = "RunCmd.py -p " + sub_project_folder + ' echo \"' + str(self.model_start_year) + ' ' + str(self.model_start_month) + ' ' + str(self.model_start_day) + ' print_daily_on\" > ' + output_location
            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->RunCmd")
            self.logger.error(str(e))
            return -1138

    def RunModelOptions(self, options):
        try:

            my_command = "RunModel.py " + options

            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception,e:
            self.logger.info("FAILED->RunModelOptions")
            self.logger.error(str(e))
            return -1139
        
    ##TODO MORE OPTIONS
    def RunModel(self, sub_project_folder):
        try:

            model_start = str(self.model_start_year) + ' ' + str(self.model_start_month) + ' ' + str(self.model_start_day) + ' 1'
            model_end = str(self.model_end_year) + ' ' + str(self.model_start_month) + ' ' + str(self.model_end_day) + ' 1'

            my_command = "RunModel.py -v -p " + sub_project_folder + ' -d "Test model run" --basin -pre test -st ' + model_start + ' -ed ' + model_end + ' -w world -t tec_daily.txt -r world.flow -- -s 0.07041256017 133.552915269 1.81282283058 -sv 4.12459677088 78.3440566535 -gw 0.00736592779294 0.340346799457'


            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            self.logger.info("FAILED->RunModel")
            self.logger.error(str(e))
            return -1140

    def RHESSysPlot(self, sub_project_folder, obs_data):
        try:
            data = sub_project_folder + '/rhessys/output/test/rhessys_basin.daily'
            my_command = "RHESSysPlot.py --plottype standard -o " + obs_data + " -d " + data + " -c streamflow --secondaryData " + data + ' --secondaryColumn precip --secondaryLabel "Rainfall (mm/day)" -t "DR5 streamflow" -l "Test simulation" -f test_plot --figureX 8 --figureY 3 -y "Streamflow (mm/day)" --color magenta'

            self.logger.info(my_command)
            output = subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT, cwd=sub_project_folder)
            return output
        except Exception as e:
            self.logger.info("FAILED->RHESSysPlot")
            self.logger.error(str(e))
            return -1141

    ###############################################################################################
    ### Functions to execute HydroTerre Workflows

    def set_huc12_list(self, huc_list_as_string):
        try:
            self.huc_list = huc_list_as_string.split(';')
            self.huc_list_count = len(self.huc_list)
        except Exception as e:
            self.logger.info("FAILED->set_huc12_list")
            self.logger.error(str(e))
            return -1142


    def get_HUC12_IDs_from_RhyessSys_Domain(self, extent):
    
        try:
            XMin = extent.min_x
            YMin = extent.min_y
            XMax = extent.max_x
            YMax = extent.max_y

            huc_list_result = ""
    
            check_interval=30
            taskUrl = "http://hydroterre.psu.edu:6080/arcgis/rest/services/RHESSys/getHUC12sfromRHESSysWorkflows/GPServer/get_HUC12_IDs_from_Extent"
    
            ###############################################################################################
            # Call HydroTerre Service
    
            data = {'XMin': XMin,
                    'YMin' : YMin,
                    'XMax' : XMax,
                    'YMax' : YMax,
                    'f': 'pjson'}
    
            submitUrl = taskUrl + "/submitJob"
    
            submitResponse = urllib.urlopen(submitUrl, urllib.urlencode(data))   
            submitJson = json.loads(submitResponse.read())    
    
            ###############################################################################################
            # Check for HydroTerre Service results
    
            if 'jobId' in submitJson:  
                jobID = submitJson['jobId']        
                status = submitJson['jobStatus']        
                jobUrl = taskUrl + "/jobs/" + jobID            
                    
                while status == "esriJobSubmitted" or status == "esriJobExecuting":
                    print("checking to see if HydroTerre job is completed...")
                    time.sleep(check_interval)
                    
                    jobResponse = urllib.urlopen(jobUrl, "f=json")     
                    jobJson = json.loads(jobResponse.read())
                 
                    if 'jobStatus' in jobJson:  
                        status = jobJson['jobStatus']            
                     
                        if status == "esriJobSucceeded":                                        
                                if 'results' in jobJson:
                                    resultsUrl = jobUrl + "/results/"
                                    resultsJson = jobJson['results']
                                    for paramName in resultsJson.keys():
                                        #print paramName
                                        resultUrl = resultsUrl + paramName                                        
                                        resultResponse = urllib.urlopen(resultUrl, "f=json")   
                                        resultJson = json.loads(resultResponse.read())                            
                                        #print resultJson['value']
                                        if paramName == 'Result_HUC12_List':
                                            huc_list_result = resultJson['value']
     
                                    #print resultsJson['Result_HUC12_List']
                 
                                #print jobJson
    
                        if status == "esriJobFailed":                                        
                                if 'messages' in jobJson:                        
                                    self.logger.error(jobJson['messages'])
                                    self.logger.error('HydroTerre job failed get_HUC12_IDs_from_RhyessSys_Domain')
                                    sys.exit(-1143)
                                                       
            else:
                self.logger.info("FAILED->get_HUC12_IDs_from_RhyessSys_Domain")
                self.logger.error("no HydroTerre jobId found in the response get_HUC12_IDs_from_RhyessSys_Domain")
                sys.exit(-1144)
    
        except Exception as e:
            self.logger.info("FAILED->get_HUC12_IDs_from_RhyessSys_Domain")
            self.logger.error( str(e) )
        
        self.set_huc12_list(huc_list_result)    
        self.logger.info(huc_list_result)

        return huc_list_result


    def HydroTerre_RHESSys_ByExtent(self, extent, ht_start_date, ht_end_date, output_folder_location):

        try:
            url_result = ""
            check_interval=30
            XMin = extent.min_x
            YMin = extent.min_y
            XMax = extent.max_x
            YMax = extent.max_y

            ###############################################################################################
            # Call HydroTerre Service

            data = {'XMin': XMin,
                    'YMin': YMin,
                    'XMax': XMax,
                    'YMax': YMax,
                    'Start_Date' : ht_start_date,
                    'End_Date' : ht_end_date,
                    'f': 'pjson'}

            taskUrl = "http://hydroterre.psu.edu:6080/arcgis/rest/services/RHESSys/HydroTerre_RHESSys_ByExtent/GPServer/HydroTerre_Rhessys_By_Extent"
            submitUrl = taskUrl + "/submitJob"

            submitResponse = urllib.urlopen(submitUrl, urllib.urlencode(data))   
            submitJson = json.loads(submitResponse.read())    

            ###############################################################################################
            # Check for HydroTerre Service results

            if 'jobId' in submitJson:  
                jobID = submitJson['jobId']        
                status = submitJson['jobStatus']        
                jobUrl = taskUrl + "/jobs/" + jobID            
                    
                while status == "esriJobSubmitted" or status == "esriJobExecuting":
                    print("checking to see if HydroTerre job is completed...")
                    time.sleep(check_interval)
                    
                    jobResponse = urllib.urlopen(jobUrl, "f=json")     
                    jobJson = json.loads(jobResponse.read())
                 
                    if 'jobStatus' in jobJson:  
                        status = jobJson['jobStatus']            
                     
                        if status == "esriJobSucceeded":                                        
                                if 'results' in jobJson:
                                    resultsUrl = jobUrl + "/results/"
                                    resultsJson = jobJson['results']
                                    for paramName in resultsJson.keys():
                                        #print paramName
                                        resultUrl = resultsUrl + paramName                                        
                                        resultResponse = urllib.urlopen(resultUrl, "f=json")   
                                        resultJson = json.loads(resultResponse.read())

                                        if paramName == 'Result_URL':
                                             url_result = resultJson['value']

                                        if paramName == 'HUC12_AREAS':
                                             huc12areas = resultJson['value']
                 
                                #print jobJson
                        if status == "esriJobFailed":                                        
                                if 'messages' in jobJson:                        
                                    print(jobJson['messages'])
                                    print('HydroTerre job failed')
                                    sys.exit(-1145)
                                                       
            else:
                self.logger.info("FAILED->HydroTerre_RHESSys_ByExtent")
                print("no HydroTerre jobId found in the response")
                sys.exit(-1146)

            ###############################################################################################
            # Get HydroTerre Service Data Bundle

            print('--------Download Start-------------')
            print('Retrieving result from: '+ url_result)
            wget.download(url_result, out=output_folder_location)
            print('--------Download End-------------')
            
            ###############################################################################################
            #print '--------Unzip Start-------------'
            zipfolder = output_folder_location + '/RHESSys_ETV'
            self.create_path(zipfolder)
            zipfilepathname = output_folder_location + '/RHESSys_ETV_Data.zip'
            self.unzip_etv_zip_file_at_path(zipfilepathname, zipfolder)
            #print '--------Unzip End-------------'

            ###############################################################################################
            print('--------HUC12 Area-------------')
            print(huc12areas + ' SQKM')
            self.areaEstimate = huc12areas


        except Exception as e:
            self.logger.info("FAILED->HydroTerre_RHESSys_ByExtent")
            print(str(e))

            
        return

    ###############################################################################################
    ### EXECUTE

    def execute_workflow(self):
        try:
            self.start_time = datetime.datetime.now()
            self.logger.info(self.start_time)

            self.logger.info("get_NHDStreamflowGageIdentifiersAndLocation")
            output = self.get_NHDStreamflowGageIdentifiersAndLocation(self.sub_project_folder,self.gageid)
            if output < 0:
                sys.exit(-1147)
            self.logger.info(output)

            self.logger.info("get_CatchmentShapefileForNHDStreamflowGage")
            output = self.get_CatchmentShapefileForNHDStreamflowGage(self.sub_project_folder)
            if output < 0:
                sys.exit(-1148)
            self.logger.info(output)

            self.logger.info("get_BoundingboxFromStudyareaShapefile")
            output = self.get_BoundingboxFromStudyareaShapefile(self.sub_project_folder)
            if output < 0:
                sys.exit(-1149)
            self.logger.info(output)

            ## Now can get extent
            self.logger.info("get_Extent_from_RHESSysWorkflows_Metadata_File")
            self.extent = self.get_Extent_from_RHESSysWorkflows_Metadata_File()
            if self.extent < 0:
                sys.exit(-1150)

            ## Now get huc12 list count (threshold too big?)
            ##self.logger.info("get_Extent_from_RHESSysWorkflows_Metadata_File")
            ##self.huc_list_as_string = self.get_HUC12_IDs_from_RhyessSys_Domain(self.extent)
            ##self.logger.info("huc_list = " + huc_list_as_string)


##TODO Add GSSURGO back to HT workflow

            ## Get Data Bundle (will need to have internal threshold check for now)
            self.logger.info("get_Extent_from_RHESSysWorkflows_Metadata_File")
            output = self.HydroTerre_RHESSys_ByExtent(self.extent, self.ht_start_date, self.ht_end_date, self.sub_project_folder)
            self.logger.info(output)

            print('--------Unzip Start-------------')
            zipfolder = self.sub_project_folder + '/RHESSys_ETV'
            self.create_path(zipfolder)
            zipfilepathname = self.sub_project_folder + '/RHESSys_ETV_Data.zip'
            self.unzip_etv_zip_file_at_path(zipfilepathname, zipfolder)
            print('--------Unzip End-------------')

##TODO ERROR MESSAGE -> NEED TO RETURN MEANINGFUL MESSAGES FROM SERVICE. i.e. return message when too many huc12s

  
            self.logger.info("get_USGSDEMForBoundingbox")
            output = self.get_USGSDEMForBoundingbox(self.sub_project_folder)
            if output < 0:
                sys.exit(-1151)
            self.logger.info(output)

            self.logger.info("get_USGSNLCDForDEMExtent")
            output = self.get_USGSNLCDForDEMExtent(self.sub_project_folder)
            if output < 0:
                sys.exit(-1152)
            self.logger.info(output)

 
            self.logger.info("get_SSURGOFeaturesForBoundingbox")
            output = self.get_SSURGOFeaturesForBoundingbox(self.sub_project_folder)
            if output< 0:
                sys.exit(-1153)
            self.logger.info(output)


            self.logger.info("GenerateSoilPropertyRastersFromSSURGO")
            output = self.GenerateSoilPropertyRastersFromSSURGO(self.sub_project_folder)
            if output < 0:
                sys.exit(-1154)
            self.logger.info(output)


            #TODO
            #self.lai_fullpathname_with_ext = "/projects/start_from_scratch/01589312/static_lai-01589312.tif"

            #How do I handle array of LAI rasters for workflow?
            #Resampling lai raster from EPSG:4269 to EPSG:32618, spatial resolution
            self.logger.info("Register_LAI_Raster")
            self.lai_fullpathname_with_ext = self.sub_project_folder + '/RHESSys_ETV/RHESSys_LAI/LAI_Month0.tif'
            
            output = self.Register_LAI_Raster(self.sub_project_folder, self.lai_fullpathname_with_ext, self.publisher)
            if output < 0:
                sys.exit(-1155)
            self.logger.info(output)

            self.logger.info("CreateGRASSLocationFromDEM")
            #Beware of quotes
            output = self.CreateGRASSLocationFromDEM(self.sub_project_folder, '"RHESSys model for Dead Run 5 watershed near Catonsville, MD"')
            if output < 0:
                sys.exit(-1156)
            self.logger.info(output)

#TODO CHECK SOURCE PATH IS VALID
            self.logger.info("ImportRHESSysSource")
            output = self.ImportRHESSysSource(self.sub_project_folder, self.rhessys_source_location)
            if output < 0:
                sys.exit(-1157)
            self.logger.info(output)


##NOTE ASSUMPTION ABOUT PATH
            self.climate_data_fullpathname = self.sub_project_folder + '/RHESSys_ETV/RHESSys_Climate'


#PROBLEM HERE
            self.logger.info("ImportClimateData")
            output = self.ImportClimateData(self.sub_project_folder, self.climate_data_fullpathname)
            if output < 0:
                sys.exit(-1158)
            self.logger.info(output)


##NOTE ASSUMPTION ABOUT PATH
            self.station_data_fullpathname = self.sub_project_folder + '/RHESSys_ETV/RHESSys_Climate'


##TODO Does USGS provide CONUS location of climate stations we can use?
##TODO Do we need this function to continue?

            #self.logger.info("GenerateBaseStationMap")
            #output = self.GenerateBaseStationMap(self.sub_project_folder, self.station_data_fullpathname)
            #if output == -1:
            #    sys.exit(-1013)
            #self.logger.info(output)


            #TODO OTHER METHODS TO ESTIMATE AREA (i.e from huc12s).
            #POOR self.areaEstimate = self.extent.area

            self.logger.info("DelineateWatershed")
            output = self.DelineateWatershed(self.sub_project_folder, self.dem_cell_threshold, self.areaEstimate)
            if output < 0:
                sys.exit(-1159)
            self.logger.info(output)


##TODO Other Options
            self.logger.info("GeneratePatchMap")
            output = self.GeneratePatchMap(self.sub_project_folder)
            if output < 0:
                sys.exit(-1160)
            self.logger.info(output)

            self.logger.info("GenerateSoilTextureMap")
            output = self.GenerateSoilTextureMap(self.sub_project_folder)
            if output < 0:
                sys.exit(-1161)
            self.logger.info(output)

            self.logger.info("ImportRasterMapIntoGRASS_LAI")
            output = self.ImportRasterMapIntoGRASS_LAI(self.sub_project_folder)
            if output < 0:
                sys.exit(-1162)
            self.logger.info(output)

            self.logger.info("ImportRasterMapIntoGRASS_LANDCOVER")
            output = self.ImportRasterMapIntoGRASS_LANDCOVER(self.sub_project_folder)
            #if output < 0:
            #    sys.exit(-1163)
            self.logger.info(output)

#            self.logger.info("ImportRasterMapIntoGRASS_LANDCOVER")
#            output = #self.ImportRasterMapIntoGRASS_LANDCOVER(self.sub_project_folder)
#            #if output < 0:
#            #    sys.exit(-1164)
#            self.logger.info(output)


            self.logger.info("RegisterLandcoverReclassRules")
            output = self.RegisterLandcoverReclassRules(self.sub_project_folder)
            if output < 0:
                sys.exit(-1165)
            self.logger.info(output)

            self.logger.info("GenerateLandcoverMaps")
            output = self.GenerateLandcoverMaps(self.sub_project_folder)
            if output < 0:
                sys.exit(-1166)
            self.logger.info(output)

#TODO VARIABLE NAMES
            self.logger.info("GenerateWorldTemplate")
            output = self.GenerateWorldTemplate(self.sub_project_folder)
            if output < 0:
                sys.exit(-1167)
            self.logger.info(output)

            self.logger.info("CreateWorldfile")
            output = self.CreateWorldfile(self.sub_project_folder)
            if output < 0:
                sys.exit(-1168)
            self.logger.info(output)

            self.logger.info("CreateFlowtable")
            output = self.CreateFlowtable(self.sub_project_folder)
            if output < 0:
                sys.exit(-1169)
            self.logger.info(output)

            self.logger.info("RunLAIRead")
            output = self.RunLAIRead(self.sub_project_folder)
            if output < 0:
                sys.exit(-1170)
            self.logger.info(output)

            self.logger.info("RunCmd")
            addmonths = 9
            output = self.RunCmd(self.sub_project_folder,addmonths)
            #output = self.RunCmd(self.sub_project_folder)
            if output < 0:
                sys.exit(-1171)
            self.logger.info(output)

            self.logger.info("RunModel")
            output = self.RunModel(self.sub_project_folder)
            #if output < 0:
            #    sys.exit(-1172)
            self.logger.info(output)

            self.logger.info("RHESSysPlot")
            obs_data = '/projects/start_from_scratch/01589312/DR5_discharge_WY2008-2012.txt'
            output = self.RHESSysPlot(self.sub_project_folder, obs_data)
            self.logger.info(output)



            self.end_time = datetime.datetime.now()
            self.logger.info(self.end_time)

            self.timespan = self.end_time - self.start_time
            self.logger.info("Workflow took: " + self.timespan)
 
        except Exception as e:
            self.logger.info("FAILED->execute_workflow")
            return str(e)



    ###############################################################################################
    ### Print this object
    def __repr__(self):

        result = "-- INPUTS ------------------------------------------------------------\n"
        result += "Project location = " + str(self.project_location) + "\n"
        result += "Project name = " + str(self.project_name) + "\n"
        result += "Gage Id = " + str(self.gageid) + "\n"
        result += "HT Start date = " + str(self.ht_start_date) + "\n"
        result += "HT End date = " + str(self.ht_end_date) + "\n"

        result += "-- PROPERTIES ------------------------------------------------------------\n"
        result += "Project Extent" + str(self.extent) + "\n"
        result += "HUC-12 Count = " + str(self.huc_list_count) + "\n"
        result += "HUC-12 AREA = " + str(self.areaEstimate) + "\n"

        result += "-- TIME------------------------------------------------------------\n"
        result += "Workflow Start time = " + str(self.start_time) + "\n"
        result += "Workflow End time = " + str(self.end_time) + "\n"
        result += "Workflow Timespan = " + str(self.timespan) + "\n"
 
        return result
