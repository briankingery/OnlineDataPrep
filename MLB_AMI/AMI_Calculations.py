#-------------------------------------------------------------------------------
# Name:         AMI_Calculations.py
#
# Purpose:      Calculate the AMI by team and by position.
#
# Author:       Brian Kingery
#
# Created:      9/9/2016
# 
# MLB Air Mile Index - Casecade Story Map
# http://arcg.is/2c1Rj8G
#-------------------------------------------------------------------------------

import arcpy
from arcpy import env

env.workspace = r'C:\Users\bkingery\Desktop\Baseball\Baseball.gdb'
env.overwriteoutput = True

teams = []
positions = []

fc = r'C:\Users\bkingery\Desktop\Baseball\Baseball.gdb\Player_Lines'
fields = ['TEAM', 'AirMileIndex', 'POS']

cursor1 = arcpy.SearchCursor(fc)
for row in cursor1:
    if row.getValue(fields[0]) in teams:
        pass
    else:
        teams.append(row.getValue(fields[0]))

cursor2 = arcpy.SearchCursor(fc)
for row in cursor2:
    if row.getValue(fields[2]) in positions:
        pass
    else:
        positions.append(row.getValue(fields[2]))


##for team in sorted(teams):
##    print team
##for position in sorted(positions):
##    print position

dictTeam = {}

for team in sorted(teams):
    
    expression = arcpy.AddFieldDelimiters(env.workspace, "TEAM") + " = '" + team + "'"
    totalAMI = 0
    playerCount = 0
    with arcpy.da.SearchCursor(fc, fields, where_clause = expression) as cursor:
        for row in cursor:
            totalAMI += row[1]
            playerCount +=1

        AVG = totalAMI / playerCount

        #Add to dictionary
        dictTeam[team] = AVG
        print team + ',',
        print str(AVG) + ',',
        print str(totalAMI) + ',',
        print str(playerCount)

dictPosition = {}
for position in sorted(positions):
    
    expression = arcpy.AddFieldDelimiters(env.workspace, "POS") + " = '" + position + "'"
    totalAMI = 0
    playerCount = 0
    with arcpy.da.SearchCursor(fc, fields, where_clause = expression) as cursor:
        for row in cursor:
            totalAMI += row[1]
            playerCount +=1

        AVG = totalAMI / playerCount

        #Add to dictionary
        dictPosition[position] = AVG
        print position + ',',
        print str(AVG) + ',',
        print str(totalAMI) + ',',
        print str(playerCount)
