import os
import shutil

from docker.rhessys_wf import *

project_location = './test'
project_name = 'mytest'
gageid = '01589312'
start_date = '2008-01-01'
end_date = '2010-01-01'
rhessys_source_location = ''
publisher = 'RHESSysWorkflow'

# remove project directory
if os.path.exists(project_location):
    raw_input('Project directory already exists, press any key to remove')
    shutil.rmtree(project_location)

w = RHESSysWorkflow(project_location, project_name, gageid, start_date, end_date, rhessys_source_location, publisher)

o = w.get_NHDStreamflowGageIdentifiersAndLocation(w.sub_project_folder,w.gageid)
print o

o = w.get_CatchmentShapefileForNHDStreamflowGage(w.sub_project_folder)
print o

o = w.get_BoundingboxFromStudyareaShapefile(w.sub_project_folder)
print o

extent = w.get_Extent_from_RHESSysWorkflows_Metadata_File()
print extent

o = w.HydroTerre_RHESSys_ByExtent(extent, w.ht_start_date, w.ht_end_date, w.sub_project_folder)
print o
zipfolder = w.sub_project_folder + '/RHESSys_ETV'
w.create_path(zipfolder)
zipfilepathname = w.sub_project_folder + '/RHESSys_ETV_Data.zip'
w.unzip_etv_zip_file_at_path(zipfilepathname, zipfolder)

o = w.get_USGSDEMForBoundingbox(w.sub_project_folder)
print o

o = w.get_USGSNLCDForDEMExtent(w.sub_project_folder)
print o

o = w.get_SSURGOFeaturesForBoundingbox(w.sub_project_folder)
print o

o = w.GenerateSoilPropertyRastersFromSSURGO(w.sub_project_folder)
print o

w.lai_fullpathname_with_ext = w.sub_project_folder + '/RHESSys_ETV/RHESSys_LAI/LAI_Month0.tif'
o = w.Register_LAI_Raster(w.sub_project_folder, w.lai_fullpathname_with_ext, w.publisher)
print o

o = w.CreateGRASSLocationFromDEM(w.sub_project_folder, '"RHESSys model for Dead Run 5 watershed near Catonsville, MD"')
print o

output = w.ImportRHESSysSource(w.sub_project_folder)


raw_input('Press any key to run: ImportClimateData')
w.climate_data_fullpathname = w.sub_project_folder + '/RHESSys_ETV/RHESSys_Climate'
o = w.ImportClimateData(w.sub_project_folder, w.climate_data_fullpathname)
w.station_data_fullpathname = w.sub_project_folder + '/RHESSys_ETV/RHESSys_Climate'
print o

raw_input('Press any key to run: DelineateWatershed')
o = w.DelineateWatershed(w.sub_project_folder, w.dem_cell_threshold, w.areaEstimate)
print o

raw_input('Press any key to run: GeneratePatchMap')
o = w.GeneratePatchMap(w.sub_project_folder)
print o

raw_input('Press any key to run: GenerateSoilTextureMap')
o = w.GenerateSoilTextureMap(w.sub_project_folder)
print o

