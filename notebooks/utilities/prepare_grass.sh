#!/bin/sh
#This program is Free Software under the GNU GPL (>=v2).
# create a new LOCATION from a raster data set

#variables to customize:
GISBASE=/usr/lib/grass64
GISDBASE=/home/jovyan/grassdata
GRASS_ADDON_PATH=/home/jovyan/work/notebooks/.grass6/addons

wget https://www.hydroshare.org/django_irods/download/3d74dccef69649b3a271d1c76f36d310/data/contents/static_lai-01589312.tif -O map.tif

MAP=map.tif
LOCATION=$1

#nothing to change below:
if [ $# -lt 1 ] ; then
 echo "Script to create a new LOCATION from a raster data set"
 echo "Usage:"
 echo "   create_location.sh location_name"
 exit 1
fi

#generate temporal LOCATION:
TEMPDIR=$$.tmp
mkdir -p $GISDBASE/$TEMPDIR/temp

#save existing $HOME/.grassrc6
if test -e $HOME/.grassrc6 ; then
   mv $HOME/.grassrc6 /tmp/$TEMPDIR.grassrc6
fi

echo "LOCATION_NAME: $TEMPDIR"  >  $HOME/.grassrc6
echo "MAPSET: temp"                 >> $HOME/.grassrc6
echo "DIGITIZER: none"              >> $HOME/.grassrc6
echo "GISDBASE: $GISDBASE"          >> $HOME/.grassrc6
export GISBASE=$GISBASE
export GISRC=$HOME/.grassrc6
export PATH=$PATH:$GISBASE/bin:$GISBASE/scripts

# import raster map into new location:
r.in.gdal -oe in=$MAP out=$MAP location=$LOCATION
if [ $? -eq 1 ] ; then
  echo "An error occured. Stop."
  exit 1
fi

#restore saved $HOME/.grassrc6
if test -f /tmp/$TEMPDIR.grassrc6 ; then
   mv /tmp/$TEMPDIR.grassrc6 $HOME/.grassrc6
fi
echo $GRASS_ADDON_PATH

echo "LOCATION_NAME: $LOCATION"  >  $HOME/.grassrc6
echo "MAPSET: PERMANENT"                 >> $HOME/.grassrc6
echo "DIGITIZER: none"              >> $HOME/.grassrc6
echo "GISDBASE: $GISDBASE"          >> $HOME/.grassrc6
export GISRC=$HOME/.grassrc6

#grass64 -text /home/jovyan/work/notebooks/$LOCATION/PERMANENT
g.extension extension=r.soils.texture prefix=$GRASS_ADDON_PATH
g.extension extension=r.findtheriver prefix=$GRASS_ADDON_PATH

echo "Now launch GRASS with:"
echo " grass64 $GISDBASE/$LOCATION/PERMANENT"
