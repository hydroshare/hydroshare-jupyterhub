#!/bin/sh
#This program is Free Software under the GNU GPL (>=v2).
# create a new LOCATION from a raster data set

#variables to customize:
GISBASE=/usr/lib/grass72
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

#save existing $HOME/.grass7
if test -e $HOME/.grass7 ; then
   mv $HOME/.grass7 /tmp/$TEMPDIR.grass7
fi

echo "LOCATION_NAME: $TEMPDIR"  >  $HOME/.grass7
echo "MAPSET: temp"                 >> $HOME/.grass7
echo "DIGITIZER: none"              >> $HOME/.grass7
echo "GISDBASE: $GISDBASE"          >> $HOME/.grass7
export GISBASE=$GISBASE
export GISRC=$HOME/.grass7
export PATH=$PATH:$GISBASE/bin:$GISBASE/scripts

# import raster map into new location:
r.in.gdal -oe in=$MAP out=$MAP location=$LOCATION
if [ $? -eq 1 ] ; then
  echo "An error occured. Stop."
  exit 1
fi

#restore saved $HOME/.grass7
if test -f /tmp/$TEMPDIR.grass7 ; then
   mv /tmp/$TEMPDIR.grass7 $HOME/.grass7
fi
echo $GRASS_ADDON_PATH

echo "LOCATION_NAME: $LOCATION"  >  $HOME/.grass7
echo "MAPSET: PERMANENT"                 >> $HOME/.grass7
echo "DIGITIZER: none"              >> $HOME/.grass7
echo "GISDBASE: $GISDBASE"          >> $HOME/.grass7
export GISRC=$HOME/.grass7

#grass72 -text /home/jovyan/work/notebooks/$LOCATION/PERMANENT
g.extension extension=r.soils.texture prefix=$GRASS_ADDON_PATH
g.extension extension=r.findtheriver prefix=$GRASS_ADDON_PATH

echo "Now launch GRASS with:"
echo " grass72 $GISDBASE/$LOCATION/PERMANENT"
