#-------------------------------------------------------------------------------
# Name:         Baseball_Lines.py
#
# Purpose:      Query the AMI lines for each team and for each position to be
#               able to upload data that can be used in a free ArcGIS Online account.
#
# Author:       Brian Kingery
#
# Created:      9/12/2016
# 
# MLB Air Mile Index - Casecade Story Map
# http://arcg.is/2c1Rj8G
#-------------------------------------------------------------------------------

import arcpy, time, datetime, string, zipfile, sys, os, glob
from arcpy import env

env.workspace = r'C:\Users\bkingery\Desktop\Baseball\Baseball.gdb'
env.overwriteoutput = True

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
SHP_Folder = r"C:\Users\bkingery\Desktop\Baseball\Files\SHP\TeamLines\SHP"
if arcpy.Exists(SHP_Folder):
    arcpy.Delete_management(SHP_Folder)
## Create SHP Folder
if not os.path.exists(SHP_Folder):
    os.makedirs(SHP_Folder)
## Delete ZIP folder so duplicates are not created
ZIP_Folder = r"C:\Users\bkingery\Desktop\Baseball\Files\SHP\TeamLines\ZIP"
if arcpy.Exists(ZIP_Folder):
    arcpy.Delete_management(ZIP_Folder)
## Create SHP Folder
if not os.path.exists(ZIP_Folder):
    os.makedirs(ZIP_Folder)

## Delete SHP folder so duplicates are not created
SHP_Folder2 = r"C:\Users\bkingery\Desktop\Baseball\Files\SHP\PositionLines\SHP"
if arcpy.Exists(SHP_Folder2):
    arcpy.Delete_management(SHP_Folder2)
## Create SHP Folder
if not os.path.exists(SHP_Folder2):
    os.makedirs(SHP_Folder2)
## Delete ZIP folder so duplicates are not created
ZIP_Folder2 = r"C:\Users\bkingery\Desktop\Baseball\Files\SHP\PositionLines\ZIP"
if arcpy.Exists(ZIP_Folder2):
    arcpy.Delete_management(ZIP_Folder2)
## Create SHP Folder
if not os.path.exists(ZIP_Folder2):
    os.makedirs(ZIP_Folder2)

teams = []
positions = []

fc = r'C:\Users\bkingery\Desktop\Baseball\Baseball.gdb\Player_Lines'

field = "TEAM"
cursor = arcpy.SearchCursor(fc)
for row in cursor:
    if row.getValue(field) in teams:
        pass
    else:
        teams.append(row.getValue(field))

field2 = "POS"
cursor2 = arcpy.SearchCursor(fc)
for row in cursor2:
    if row.getValue(field2) in positions:
        pass
    else:
        positions.append(row.getValue(field2))

for team in sorted(teams):
    # Set local variables
    inFeatures = fc
    outLocation = r'C:\Users\bkingery\Desktop\Baseball\Baseball.gdb\TeamLines'
    outFeatureClass = team.replace(" ","_").replace(".","")
    delimitedField = arcpy.AddFieldDelimiters(env.workspace, "TEAM")
    expression = delimitedField + " = '" + team + "'"
    # Execute FeatureClassToFeatureClass
    arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass, expression)
    print "Copied:", outFeatureClass

for position in sorted(positions):
    # Set local variables
    inFeatures = fc
    outLocation = r'C:\Users\bkingery\Desktop\Baseball\Baseball.gdb\PositionLines'
    if position == '1B':
        outFeatureClass = 'First_Base'
    elif position == '2B':
        outFeatureClass = 'Second_Base'
    elif position == '3B':
        outFeatureClass = 'Third_Base'
    elif position == 'C':
        outFeatureClass = 'Catcher'
    elif position == 'CF':
        outFeatureClass = 'Center_Field'
    elif position == 'DH':
        outFeatureClass = 'Designated_Hitter'
    elif position == 'LF':
        outFeatureClass = 'Left_Field'
    elif position == 'RF':
        outFeatureClass = 'Right_Field'
    elif position == 'RP':
        outFeatureClass = 'Relief_Pitcher'
    elif position == 'SP':
        outFeatureClass = 'Starting_Pitcher'
    elif position == 'SS':
        outFeatureClass = 'Shortstop'
    delimitedField = arcpy.AddFieldDelimiters(env.workspace, "POS")
    expression = delimitedField + " = '" + position + "'"
    # Execute FeatureClassToFeatureClass
    arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass, expression)
    print "Copied:", outFeatureClass

## Cycle through all datasets and their feature classes 
dataset_list = arcpy.ListDatasets("TeamLines")
for dataset in dataset_list:
    fc_in_dataset_list = arcpy.ListFeatureClasses("","",dataset)
    for fc in fc_in_dataset_list:
        ## Set local variables
        inFeatures = fc
        ## Execute FeatureClassToShapefile
        arcpy.FeatureClassToShapefile_conversion(inFeatures, SHP_Folder)
        print "Converted: " + fc

## Cycle through all datasets and their feature classes 
dataset_list = arcpy.ListDatasets("PositionLines")
for dataset in dataset_list:
    fc_in_dataset_list = arcpy.ListFeatureClasses("","",dataset)
    for fc in fc_in_dataset_list:
        ## Set local variables
        inFeatures = fc
        ## Execute FeatureClassToShapefile
        arcpy.FeatureClassToShapefile_conversion(inFeatures, SHP_Folder2)
        print "Converted: " + fc

## Change workspace to SHP folder
env.workspace = SHP_Folder
## Cycle through all shapefiles and zip
shpList = arcpy.ListFeatureClasses()
for shp in shpList:
    x = SHP_Folder + os.sep + shp
    y = ZIP_Folder + os.sep + shp[:-3]+"zip"
    zipShapefile(x,y)

## Change workspace to SHP folder
env.workspace = SHP_Folder2
## Cycle through all shapefiles and zip
shpList = arcpy.ListFeatureClasses()
for shp in shpList:
    x = SHP_Folder2 + os.sep + shp
    y = ZIP_Folder2 + os.sep + shp[:-3]+"zip"
    zipShapefile(x,y)

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "\nEnded: %s\n" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]
