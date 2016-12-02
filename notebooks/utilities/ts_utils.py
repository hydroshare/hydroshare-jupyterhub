from __future__ import print_function
import os, sys
from IPython.core.display import display, HTML  
import shutil
import requests
import threading
import glob
import math
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, AutoDateFormatter, AutoDateLocator

from . import hs_utils

is_py2 = sys.version[0] == '2'
if not is_py2:
    msg = 'The ts_utils function currently only works with Python 2.X'
    raise Exception(msg)
else:
    # set this for future python3 compatibility
    input = raw_input
    
    from odm2api.ODMconnection import dbconnection
    from odm2api.ODM2.services.readService import *
    from odm2api.ODM2.services.createService import *

class timeseries():
    def __init__(self):
        self.hydroshare = hs_utils.hydroshare()
        self.odm2db = None
        self._session = None
        self.read = None
        self.write = None
        self.tsresults = {}
        self.tsvalues = {}
        
    def content(self):
        return self.hydroshare.content
    
    def loadDatabase(self):
        if self.odm2db is None:
            display(HTML('<b style="color:red">Failed to load the database. Please make sure that the content for this resource contains a *.sqlite file.'))
        
        # load odm2 database
        self._session = dbconnection.createConnection('sqlite', self.odm2db)
        self.read = ReadODM2(self._session)
        self.write = CreateODM2(self._session)
    
    def readResults(self):
        res = self.read.getResults()
        self.tsresults = {r.ResultID:r for r in res}
        return self.tsresults
    
    def readTsValues(self, ids = []):
        
        if len(self.tsresults.keys()) == 0:
            self.readResults()
            
        # assemble a list if ids to download data for
        resids = self.tsresults.keys() if len(ids) == 0 else ids
        
        # download values for each result
        for resid in resids:
            res = self.tsresults[resid]
            print('Processing -> ' + ': '.join([res.VariableObj.VariableNameCV,
                                             res.FeatureActionObj.SamplingFeatureObj.SamplingFeatureName]))
            self.tsvalues[resid] = self.read.getResultValues(resid)
            
    def previewTs(self, ids=[], rows=5):
        
        if len(self.tsresults.keys()) == 0:
            self.readResults()
            
        # assemble a list if ids to download data for
        resids = self.tsresults.keys() if len(ids) == 0 else ids

        get_ids = [tsid for tsid in resids if tsid not in self.tsvalues.keys()]
        if len(get_ids) > 0:
            print('Need to prepare the data for one or more of these result ids')
            self.readTsValues(get_ids)
        if len(get_ids) > 0 :print('\n')
        
        for tsid in resids:
            dv = self.tsvalues[tsid]['DataValue']
            dt = self.tsvalues[tsid]['ValueDateTime']
            res = self.tsresults[tsid]
            title = ' %s ' % (': '.join([res.VariableObj.VariableNameCV,
                                         res.FeatureActionObj.SamplingFeatureObj.SamplingFeatureName]))
            restext = ' ResultID: %s' % tsid
            headtext ='DataValue \t ValueDateTime'
            
            # print timeseries header
            line_len = len(title)+4
            sepline = '-'* line_len
            print('-%s-' % sepline)
            print('%s%s' % (restext,' '*(line_len-len(restext))))
            print('%s%s' % (title,' '*(line_len-len(title))))   
            print('-%s-' % sepline)
            
            # print timeseries values
            sys.stdout.write("%-25s %-25s \n" % ('DataValue','ValueDateTime'))
            for i in range(5):
                sys.stdout.write("%-25s %-25s \n" % (dt[i], dv[i]))
            print('\n')

        
    def subplotTimeSeries(self, ids=[], cols=1):
        # assemble a list if ids to download data for
        resids = self.tsresults.keys() if len(ids) == 0 else ids
        
        get_ids = [tsid for tsid in resids if tsid not in self.tsvalues.keys()]
        if len(get_ids) > 0:
            print('Need to prepare the data for one or more of these result ids')
            self.readTsValues(get_ids)
        if len(get_ids) > 0 :print('\n')
      
        # create the figure
        rows = math.ceil(float(len(resids)) / float(cols))
        fig = plt.figure(figsize=(15,rows*5))
        fig.subplots_adjust(hspace=.5)
        #fig.autofmt_xdate()
        
        #years = mdates.YearLocator()   # every year
        #months = mdates.MonthLocator()  # every month
        #days = DayLocator()              # minor ticks on the days
        #yearsFmt = mdates.DateFormatter('%Y')
        #dayFormatter = DateFormatter('%d')      # e.g., 12
        #monthFormatter = DateFormatter('%m')
            
        
        # plot the results, each in its own subplot
        for i in range(1, len(resids)+1):
            ax = fig.add_subplot(rows, cols, i)
            res = self.tsresults[resids[i-1]]
            tsval = self.tsvalues[resids[i-1]]
            
            x = list(self.tsvalues[resids[i-1]]['ValueDateTime'])
            y = list(self.tsvalues[resids[i-1]]['DataValue'])
            title = res.FeatureActionObj.SamplingFeatureObj.SamplingFeatureName
            col_width=80/cols - 4
            subtitle = title[:col_width]+' ...' if len(title) > col_width else title
            ax.set_title(subtitle, fontsize=14)

            ax.plot_date(x,y,'-')
            ax.set_ylabel(res.VariableObj.VariableNameCV + " (" + res.UnitsObj.UnitsAbbreviation + ")")
           
            locator = AutoDateLocator()
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(AutoDateFormatter(locator))
            labels = ax.get_xticklabels()
            plt.setp(labels, rotation=30, fontsize=10)
            
            # format the ticks
            #ax.xaxis.set_major_locator(years)
            #ax.xaxis.set_major_formatter(yearsFmt)
            #ax.xaxis.set_minor_locator(months)

            ax.grid(True)



    def plotTimeSeries(self, ids=[]):
        # assemble a list if ids to download data for
        resids = self.tsresults.keys() if len(ids) == 0 else ids
        
        get_ids = [tsid for tsid in resids if tsid not in self.tsvalues.keys()]
        if len(get_ids) > 0:
            print('Need to prepare the data for one or more of these result ids')
            self.readTsValues(get_ids)
        if len(get_ids) > 0 :print('\n')
      
        # create the figure
        fig = plt.figure(figsize=(15,5))
        ax = fig.add_subplot(1,1,1)        
        
        # plot the results
        for i in range(1, len(resids)+1):
            x = list(self.tsvalues[resids[i-1]]['ValueDateTime'])
            y = list(self.tsvalues[resids[i-1]]['DataValue'])
            res = self.tsresults[resids[i-1]]
            l = res.FeatureActionObj.SamplingFeatureObj.SamplingFeatureName
            ax.plot(x,y, label=l[:30])
            
            
        ax.set_ylabel(res.VariableObj.VariableNameCV + " (" + res.UnitsObj.UnitsAbbreviation + ")")
        locator = AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(AutoDateFormatter(locator))
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=30, fontsize=10)

        ax.grid(True)
            
        # add a legend
        plt.legend()
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.9))
        
        
    def getTimeSeriesResource(self, resourceid=None, destination='.'):
        """
        Downloads the content of HydroShare resource to the JupyterHub userspace

        Args:
            resourceid: id of the HydroShare resource to query
            destination: path relative to /user/[username]/notebooks/data

        """
        
        # get the resource to download. default is the id that launched jupyter
        while 1:
            if resourceid is None:
            
                res = input('It looks like you have launched JupyterHub from a resource with the id: %s.\n'
                       'Would you like to download content for this resource? [Y/n/e] ' % (os.environ['HS_RES_ID'] ))
                res_lower = res.strip().lower()
                if res_lower == 'y' or res_lower == '':
                    resourceid = os.environ['HS_RES_ID'] 
                elif res_lower == 'n':
                    resourceid = input('Enter the resource id to download: ')
                elif res_lower == 'e':
                    return None
            resourceid = str(resourceid)
            if resourceid.strip() == '':
                resourceid = os.environ['HS_RES_ID'] 

            # make sure this is a TimeSeries resource.
            try:
                res_meta = self.hydroshare.hs.getSystemMetadata(resourceid)
                
                if res_meta['resource_type'].lower() != 'timeseriesresource':
                    display(HTML('<b style="color:red;">Attempting to download resource of type %s.<br> The'
                                 '`getTimeSeriesResource` function can only be used to download resources'
                                 'of type TimeSeriesResource.<br>Please specify a TimeSeries resource to download</b>'
                                 % res_meta['resource_type']))
                else: 
                    break
                    
            except Exception as e:
                display(HTML('<b style="color:red">Failed to retrieve resource content from HydroShare: %s</b>' % e))
                return None
                    
               
                
               
        
        print('\nDownloading resource: %s' % resourceid)
        
        # set the download path
        default_dl_path = os.environ['DATA']
        dst = os.path.abspath(os.path.join(default_dl_path, destination))
        download = True
        
        # check if the data should be overwritten
        dst_res_folder = os.path.join(dst, resourceid)
        if os.path.exists(dst_res_folder):    
            res = input('This resource already exists in your userspace.\nWould you like to overwrite this data [y/N]? ')
            res_lower = res.strip().lower()
            if res == 'y':
                shutil.rmtree(dst_res_folder)
            else:
                download = False
                
        # re-download the content if desired
        if download:
            try:
                # download the resource (threaded)
                header = requests.head(res_meta['bag_url'])
                t = threading.Thread(target=self.hydroshare._getResourceFromHydroShare, 
                                     args=(resourceid,), kwargs={'destination':dst, 'unzip':True})
                hs_utils.runThreadedFunction(t, msg='Downloading', success='Download Completed Successfully')
            except Exception as e:
                display(HTML('<b style="color:red">Failed to retrieve resource content from HydroShare: %s</b>' % e))
                return None

        # load the resource content
        outdir = os.path.join(dst, '%s/%s' % (resourceid, resourceid))
        content_files = glob.glob(os.path.join(outdir,'data/contents/*'))
        
        content = {}
        for f in content_files:
            fname = os.path.basename(f)
            content[fname] = f
        
        # update the content dictionary
        self.hydroshare.content.update(content)
        
        # display the content files
        hs_utils.display_resource_content_files(self.content())
        
        # load the odm2db into memory
        try:
            # get the sqlite file associated with the resource
            odm2dbName = next(k for k in self.content().keys() if k[-6:] == 'sqlite')
            self.odm2db = self.content()[odm2dbName]
            self.loadDatabase()
        except:
            print(self.content())
            display(HTML('<b style="color:red">Failed to find a database associated with this resource.  Please make sure that the content for this resource contains a *.sqlite file.'))
            return None
        
        
        
        