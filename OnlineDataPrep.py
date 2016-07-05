'''
-------------------------------------------------------------------------------
Name:         OnlineDataPrep.py
Author:       Brian Kingery
Created:      7/5/2016

Purpose:      Cycle through a map document exporting all layers to KMZs and
              zipped shapefiles.

Directions:   Replace mxd and env.workspace variables.
              Ensure all layer names in map document have valid characters.
-------------------------------------------------------------------------------
'''

##Import
import arcpy, time, datetime, string, zipfile, sys, os, glob
from arcpy import env

## Target Locations
mxd = arcpy.mapping.MapDocument(r"\\amazon\waterworks\Divisions\InfoTech\Private\GIS_Private\Kingery\IssueTrak_Projects\HurricanePrep\2016\MXDs\2016\AGOL_Prep_Working.mxd")
env.workspace = r"\\amazon\waterworks\Divisions\InfoTech\Private\GIS_Private\Kingery\IssueTrak_Projects\HurricanePrep\2016\Data\ZipShapefile"
env.overwriteOutput = True

def zipShapefile(SHAPEFILE, ZIPFILE):
    #print "Zipping: " + SHAPEFILE
    if not (os.path.exists(SHAPEFILE)):
       print SHAPEFILE + ' Does Not Exist'
       return False
    if (os.path.exists(ZIPFILE)):
       print 'Deleting '+ZIPFILE
       os.remove(ZIPFILE)
    if (os.path.exists(ZIPFILE)):
       print 'Unable to Delete'+ZIPFILE
       return False
    zf = zipfile.ZipFile(ZIPFILE,'w')
    for FILE in glob.glob(SHAPEFILE.lower().replace(".shp",".*")):
       #print FILE
       zf.write(FILE,os.path.basename(FILE),zipfile.ZIP_DEFLATED)
    zf.close()
    return True

################################################################################
################################################################################

## Start
ExecutionStartTime = datetime.datetime.now()
print "Started: %s" % ExecutionStartTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Processing\n"

SHP_Folder = env.workspace + os.sep + "SHP"
## Delete SHP folder so duplicates are not created
if arcpy.Exists(SHP_Folder):
    arcpy.Delete_management(SHP_Folder)
## Create SHP Folder
if not os.path.exists(SHP_Folder):
    os.makedirs(SHP_Folder)
    
ZIP_Folder = env.workspace + os.sep + "ZIP"
## Delete ZIP folder so duplicates are not created
if arcpy.Exists(ZIP_Folder):
    arcpy.Delete_management(ZIP_Folder)
## Create SHP Folder
if not os.path.exists(ZIP_Folder):
    os.makedirs(ZIP_Folder)
    
fGDB = env.workspace + os.sep + "Data.gdb"
GDB = "Data.gdb"
## Delete fGDB folder so duplicates are not created
if arcpy.Exists(fGDB):
    arcpy.Delete_management(fGDB)
## Create fGDB
if not os.path.exists(fGDB):
    arcpy.CreateFileGDB_management(env.workspace, GDB)
    
KMZ_Folder = env.workspace + os.sep + "KMZ"
## Delete KMZ folder so duplicates are not created
if arcpy.Exists(KMZ_Folder):
    arcpy.Delete_management(KMZ_Folder)
## Create KMZ Folder
if not os.path.exists(KMZ_Folder):
    os.makedirs(KMZ_Folder)

lyrlist = arcpy.mapping.ListLayers(mxd)
for lyr in lyrlist:
    inFeatures = lyr
    outLocation = fGDB
    outFeatureClass = lyr.name
    # Execute FeatureClassToFeatureClass
    arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass)
    #print "LYR --> FC:",lyr.name
    # Execute LayerToKMZ
    outfile = KMZ_Folder + os.sep + lyr.name + (".kmz")    
    arcpy.LayerToKML_conversion(lyr, outfile)
    #print "LYR --> KMZ:",lyr.name
    print "Processed:",lyr.name

env.workspace = fGDB
fclist = arcpy.ListFeatureClasses()
for fc in fclist:
    inFeatures = fc
    ## Execute FeatureClassToShapefile
    arcpy.FeatureClassToShapefile_conversion(inFeatures, SHP_Folder)
    print "FC --> SHP:",fc

## Change workspace to SHP folder
env.workspace = SHP_Folder
## Cycle through all shapefiles and zip
shpList = arcpy.ListFeatureClasses()
for shp in shpList:
    x = SHP_Folder + os.sep + shp
    y = ZIP_Folder + os.sep + shp[:-3]+"zip"
    zipShapefile(x,y)
    print "Zipped:",shp

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "\nEnded: %s" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]

