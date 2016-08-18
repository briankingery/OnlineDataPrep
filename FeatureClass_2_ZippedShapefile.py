## Brian Kingery
## Oct 23, 2015
## Cycle through a workspace exporting all feature classes to a shapefile and then zipping each shapefile.

##Import
import arcpy, time, datetime, string, zipfile, sys, os, glob
from arcpy import env

## Target Locations
env.workspace = r"R:\Divisions\InfoTech\Private\GIS_Private\Kingery\ArcGIS_Online\Conway_sdeVector_sdeViewer.sde"
env.overwriteOutput = True

SHP_Folder = r"R:\Divisions\InfoTech\Private\GIS_Private\Kingery\ArcGIS_Online\SHP"
ZIP_Folder = r"R:\Divisions\InfoTech\Private\GIS_Private\Kingery\ArcGIS_Online\ZIP"

## Start
ExecutionStartTime = datetime.datetime.now()
print "Started: %s\n" % ExecutionStartTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Processing"

def zipShapefile(SHAPEFILE, ZIPFILE):
    print "Zipping: " + SHAPEFILE
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

## Delete SHP folder so duplicates are not created
if arcpy.Exists(SHP_Folder):
    arcpy.Delete_management(SHP_Folder)
## Create SHP Folder
if not os.path.exists(SHP_Folder):
    os.makedirs(SHP_Folder)
    
## Delete ZIP folder so duplicates are not created
if arcpy.Exists(ZIP_Folder):
    arcpy.Delete_management(ZIP_Folder)
## Create ZIP Folder
if not os.path.exists(ZIP_Folder):
    os.makedirs(ZIP_Folder)

## Cycle through all datasets and their feature classes 
dataset_list = arcpy.ListDatasets()
for dataset in dataset_list:
    fc_in_dataset_list = arcpy.ListFeatureClasses("","",dataset)
    for fc in fc_in_dataset_list:
        ## Set local variables
        inFeatures = fc
        ## Execute FeatureClassToShapefile
        arcpy.FeatureClassToShapefile_conversion(inFeatures, SHP_Folder)
        print "Converted: " + fc
        
## Cycle through all feature classes not in a dataset
fclist = arcpy.ListFeatureClasses()
for fc in fclist:
    ## Set local variables
    inFeatures = fc
    ## Execute FeatureClassToShapefile
    arcpy.FeatureClassToShapefile_conversion(inFeatures, SHP_Folder)
    print "Converted: " + fc
    
## Change workspace to SHP folder
env.workspace = SHP_Folder

## Cycle through all shapefiles and zip
shpList = arcpy.ListFeatureClasses()
for shp in shpList:
    x = SHP_Folder + os.sep + shp
    y = ZIP_Folder + os.sep + shp[:-3]+"zip"
    zipShapefile(x,y)

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "Ended: %s\n" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]





