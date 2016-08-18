
## Brian Kingery
## Nov 2, 2015
## Cycle through the basemap and save each layer to a ".lyr" file.
## Ensure layer names do not have any invalid characters

##Import
import arcpy, time, datetime, string, zipfile, sys, os, glob
from arcpy import env

## Target Locations
    ##It will be...
    ##env.workspace = r"N:\GIS_Private\OperationalSystems\Locations\Waterworks BaseMap\Interfaces\Layers"

env.workspace = r"C:\Users\bkingery\Desktop\BaseMap_Layers"
env.overwriteOutput = True

## Start
ExecutionStartTime = datetime.datetime.now()
print "Started: %s\n" % ExecutionStartTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Processing\n"

## Delete Layer folder so duplicates are not created
LYR_Folder = r"C:\Users\bkingery\Desktop\BaseMap_Layers\Layers"
if arcpy.Exists(LYR_Folder):
    arcpy.Delete_management(LYR_Folder)
## Create Layer Folder
if not os.path.exists(LYR_Folder):
    os.makedirs(LYR_Folder)

mxd = arcpy.mapping.MapDocument(r"C:\Users\bkingery\Desktop\BaseMap_Layers\Waterworks Network BaseMap Fixed.mxd")

## Converts all group layers to a layer file in it's own folder
for lyr in arcpy.mapping.ListLayers(mxd):
    ## Creates folders for group layers
    if lyr.isGroupLayer:
        Folder = LYR_Folder + "/" + lyr.name
        os.makedirs(Folder)

        ## Converts group layer to layer file saving it in the folder
        Group_lyr = Folder + "/" + lyr.name + ".lyr"
        arcpy.SaveToLayerFile_management(lyr, Group_lyr)

## Converts all feature layers outside of a group layer
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.isFeatureLayer:
        longname = str(lyr.longName)
        longname = string.split(longname, "\\")
        GroupLayer = longname[0]
        ## Exports all layers not in a group layer
        if lyr.longName == GroupLayer:
            Layer = LYR_Folder + "/" + lyr.name + ".lyr"
            arcpy.SaveToLayerFile_management(lyr, Layer)
        ## Exports all layers in a group layer to the folder that was created in above FOR loop
        if lyr.longName != GroupLayer:
            Layer = LYR_Folder + "/" + GroupLayer + "/" + lyr.name + ".lyr"
            arcpy.SaveToLayerFile_management(lyr, Layer)
            
del mxd

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "\nEnded: %s\n" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]

##############################################################################################
##############################################################################################
##############################################################################################


##
## Change Layer names to not have () or :
##
##Water Quality Concern Past 365 Days
##Orthophotograph Grid 2007 North
##Orthophotograph Grid 2007 South
##Orthophotograph Grid 2002
##WDS 1 250 Maps
##WDS 1 500 Maps
##System Valve Annotation 1 3000
##2 Topographic Contour
##10 Topographic Contour






##for lyr in arcpy.mapping.ListLayers(mxd):
##    ## Exports all layers not in a group layer
##    if lyr.isFeatureLayer:
##        longname = str(lyr.longName)
##        longname = string.split(longname, "\\")
##        GroupLayer = longname[0]
##        if lyr.name == GroupLayer:
##            Layer = LYR_Folder + "/" + lyr.name + ".lyr"
##            arcpy.SaveToLayerFile_management(lyr, Layer)
##
##for lyr in arcpy.mapping.ListLayers(mxd):
##    ## Creates folders for group layers
##    if lyr.isGroupLayer:
##        Folder = LYR_Folder + "/" + lyr.name
##        os.makedirs(Folder)
##
##        ## Converts group layer to layer file saving it in the folder
##        Group_lyr = Folder + "/" + lyr.name + ".lyr"
##        arcpy.SaveToLayerFile_management(lyr, Group_lyr)
##
##        ## Exports all layers in the individual group layers to the group layer folder
##        for x in lyr:
##            NestedLayer = Folder + "/" + x.name + ".lyr"
##            arcpy.SaveToLayerFile_management(lyr, NestedLayer)

