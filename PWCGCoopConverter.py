"""test for convertor for PWCG
Version 1.0
2023/07/10, Lefuneste
See https://github.com/lefufu/PylGBMiMec/blob/master/README.md
 """
import unicodedata

import pylgbmimec.basic_functions.warning_handling
from basic_functions.PWCG_PathAndIcon import getPathInfo, createFlightIcons, changeMissionComment, reduceGroupName
from basic_functions.PWCG_spawn import createSpawnLogic
from basic_functions.PWCG_startObjects import createStartLogicAll
from basic_functions.PWCG_switchAirfield import createAirfieldSwich
from basic_functions.createObjectLogic import createstartFlightLogic
from declarations.template_declaration import AIBEST, RADARNAME
# Lines started with "#" are comment
# DO NOT MODIFY the line below, they are needed to make the python working
from pylgbmimec.basic_functions.mission_class import *
from pylgbmimec.basic_functions.find_object import *
from pylgbmimec.basic_functions.modify_object import *
from pylgbmimec.basic_functions.object_creation import copy_from_mission
from pylgbmimec.basic_functions.save_mission import *
from pylgbmimec.declarations.country import *
from pylgbmimec.declarations.properties_specials import *
from pylgbmimec.basic_functions.readGlobalParameters import *
from pylgbmimec.basic_functions.PWCG_airfield import createAirfields, createMenuAirfield
import sys

#Add or Remove warnings (seems not working...)
pylgbmimec.declarations.properties_specials.WARNING_LEVEL=0

# Read default variables.
PWCGsettings=initialize_variables_from_file('settings.json')

#You can print messages on console by using "print" command as below
print("PyL2MiMec starting")
#check number of args
if len(sys.argv) != 3:
    criticalError(INVALID_INPUT_NUMER)

#get input mission name
inputMissionName = str(sys.argv[1])
outputMissionName = str(sys.argv[2])

#Read mission & template
newMission=Mission()
templateMission=Mission()

#TODO : put negative number for grups to avoid double entries
readMissionFromFile(newMission, inputMissionName)
readMissionFromFile(templateMission, "pylgbmimec/Template.Mission")

print("processing mission...")

#will display a summary of the mission contain
#print("Mission summary :")
#print(newMission)

# get existing airfield to delete them later
airField2delete = findObject(newMission, Type=AIRFIELD)

# delete waypoints icons
oldIconsList = findObject(newMission, Type=MCUICON, IconId=901)
deleteObject(newMission, oldIconsList)
# delete flight icons
#oldIconsList = findObject(newMission, Type=MCUICON, IconId=703)
#deleteObject(newMission, oldIconsList)
# delete takeoff icons
oldIconsList = findObject(newMission, Type=MCUICON, IconId=903)
deleteObject(newMission, oldIconsList)
# delete land icons
oldIconsList = findObject(newMission, Type=MCUICON, IconId=904)
deleteObject(newMission, oldIconsList)
# delete airfields
#oldIconsList = findObject(newMission, Type=MCUICON, IconId=905)
#deleteObject(newMission, oldIconsList)

#remove radar spotting if option setup
if PWCGsettings['noRadarSpotting'] == 1:
    radarList = findObject(newMission, Type=VEHICLE, Name=RADARNAME )
    set_kv(newMission, radarList, Spotter=-1)

#to be used for starting the global mission mechanism
startTriggers = list()
startAirfields = list()
groupList = list()
EscortGroup = list()
escortInfoList = dict()

flightNum = 0
#Find player's planes (=> are starting from runway)
playerPlanes=findObject(newMission, Type=PLANE, CoopStart='1')
# identify groups and loop on group (to handle more than 1 player per flight)
for playerPlaneID in playerPlanes:
    # find group of the plane
    planeGroup = findGroup(newMission, playerPlaneID)
    groupName=reduceGroupName(newMission.ObjList[planeGroup].PropList[NAME])
    groupList.append(groupName)

    #find escrot group if any
    #find the planes in the group
    Planelist=findObject(newMission, Type=PLANE, Group=groupName)
    #find escort flight: Objet of ECU cover with target on linkID of leader of escorted flight
    linkID = (newMission.ObjList[Planelist[0]]).getKv(LINKTRID)
    escortECU=findObject(newMission, Type=MCUCMDCOVER, Targets=linkID)
    if escortECU and PWCGsettings['ForcePlayerOnEscort']:
        EscortGroup = findGroup(newMission, escortECU[0])
        escortGroupName = reduceGroupName(newMission.ObjList[EscortGroup].PropList[NAME])
        escortInfoList[escortGroupName]=groupName
        groupList.append(escortGroupName)

for groupName in groupList:
    #find the planes in the group
    Planelist=findObject(newMission, Type=PLANE, Group=groupName)

    # change player plane to AI
    newMission.ObjList[playerPlaneID].setKv(COOPSTART, 0)
    # set lead AI plane as spotter, escort planes have half spotter radius
    if groupName in escortInfoList:
        newMission.ObjList[sorted(Planelist)[0]].setKv(SPOTTER, PWCGsettings['spotterRadius']/2)
    else:
        newMission.ObjList[sorted(Planelist)[0]].setKv(SPOTTER, PWCGsettings['spotterRadius'])

    #get info for path (esp. distance)
    pathInfoDict = getPathInfo(newMission, Planelist, groupName, PWCGsettings, templateMission)

    #create new spawn airfields
    createAirfields(newMission, Planelist, groupName, PWCGsettings, templateMission, pathInfoDict, escortInfoList)
    airfieldList = findObject(newMission, Type=AIRFIELD, Name=groupName)
    startAirfields.append(sorted(airfieldList)[0])

    # create counters to disable AI planes and the planeset selection logic for airfields
    createSpawnLogic(newMission, Planelist, groupName, airfieldList, PWCGsettings, templateMission, escortInfoList)

    # create airfield activation logic
    createAirfieldSwich(newMission, Planelist, groupName, airfieldList, PWCGsettings, templateMission)

    # create object activation logic when trigger takeoff
    startTrigger = createstartFlightLogic(newMission, Planelist, groupName, airfieldList, PWCGsettings, templateMission, escortInfoList)
    startTriggers.append(startTrigger)

    # TODO : fix double airstart icon
    # create icons for flight
    createFlightIcons(newMission, Planelist, groupName, PWCGsettings, templateMission, pathInfoDict, flightNum, escortInfoList)
    flightNum = flightNum+1

# MERGE start condition for all flights
createStartLogicAll(newMission, Planelist, groupList, airfieldList, PWCGsettings, templateMission, startTriggers, escortInfoList)

# change mission description
changeMissionComment(newMission, Planelist, groupList, escortInfoList,PWCGsettings)

# create fake airfield to switch to menu
createMenuAirfield(newMission, PWCGsettings, templateMission,Planelist)

#remove airfields created by PWCG
deleteObject(newMission, airField2delete)

#change mission type to dogfight
newMission.ObjList[0].setKv(MISSIONTYPE,DEATHMATCH)

#save the mission
saveMission(newMission, outputMissionName)
print('Modified mission written in '+outputMissionName)
