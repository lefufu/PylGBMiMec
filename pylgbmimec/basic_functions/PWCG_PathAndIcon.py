import math

from basic_functions.find_object import findObject, findObjectInRange
from basic_functions.mission_class import Mission
from basic_functions.modify_object import set_kv
from basic_functions.nameAndComment import createComment
from declarations.properties_specials import XPOS, ZPOS, AIRFIELD, MCUWAYPOINT, MCUCTRIGGER, YPOS, MCUICON, NAME, INDEX, SPEED, \
    LINETYPE, LCNAME, LCDESC, RCOLOR, GCOLOR, BCOLOR, ICONID, ACTIONICONID, MCULAND, \
    STARTINAIR, PLANE, SCRIPT, GUIMAP
from declarations.template_declaration import TOTALDISTANCE, LOCALDISTANCE, TARGETKEYWORD, TARGETSTATUS, PATHLINESTYLE, \
    TARGETICONNAME, CTRIGGERTAKEOFF, STARTALLCOMMENT, STARTALLNAME


# ------------------------------------------------------------------------------------------------------------------------
def getPathInfo(mission:Mission, planelist: list, groupName : str, PWCGsettings : dict ,templateMission:Mission) -> dict:
    """ collect path information  for planeset and icons"""

    totalDistance = 0.0
    prevWayp = -1
    afterTarget = 0

    pathInfo = dict()
    #browse all waypoints
    wayPointList = findObject(mission, Type=MCUWAYPOINT, Group=groupName)
    for waypoint in sorted(wayPointList):
        waypointInfo=dict()
        index = mission.ObjList[waypoint].getKv(INDEX)
        #copy info from waypoint
        for property in [NAME, XPOS, YPOS, ZPOS, SPEED] :
         waypointInfo[property]=mission.ObjList[waypoint].getKv(property)

        #conpute distance and angle from prev. waypoint
        if prevWayp == -1 :
            localDistance = 0.0
            angle = 0.0
        else :
            xDist = mission.ObjList[prevWayp].getKv(XPOS) - waypointInfo[XPOS]
            yDist = mission.ObjList[prevWayp].getKv(YPOS) - waypointInfo[YPOS]
            zDist = mission.ObjList[prevWayp].getKv(ZPOS) - waypointInfo[ZPOS]
            localDistance  = math.sqrt(xDist*xDist+yDist*yDist+zDist*zDist)

        if mission.ObjList[waypoint].getKv(NAME) == TARGETKEYWORD:
            afterTarget=1

        totalDistance =  totalDistance + localDistance
        waypointInfo[TOTALDISTANCE] = totalDistance
        waypointInfo[LOCALDISTANCE] = localDistance
        waypointInfo[TARGETSTATUS] = afterTarget

        prevWayp = waypoint
        pathInfo[index] = waypointInfo

    pathInfo[-1] = {'localDistance': 0.0, 'totalDistance': totalDistance, 'targetStatus': 0.0}

    return pathInfo

# ------------------------------------------------------------------------------------------------------------------------
def createFlightIcons(mission:Mission, planelist: list, groupName : str, PWCGsettings : dict ,templateMission:Mission, pathInfoDict:dict, flightNum:int, escortInfoList:dict) -> dict:
    """ create icons for flight """

    num=0
    if (mission.ObjList[planelist[len(planelist)-1]]).PropList[STARTINAIR] == 0 :
        airstart = 1
    else:
        airstart = 0
    #--------------------------------------------------------------------------------
    #create new icons for path
    for waypointID in sorted(pathInfoDict):
        #get info for name and comment

        #create WP icon
        templateIcon = findObject(templateMission, Type=MCUICON, IconId=901)
        iconNum = mission.MaxIndex + 1
        newIcon = templateMission.ObjList[templateIcon[0]].clone(iconNum)
        if waypointID != -1:
            #set coordinate from waypoint
            for info in [XPOS, YPOS, ZPOS]:
                newIcon.setKv(info, mission.ObjList[waypointID].getKv(info))
            name = mission.ObjList[waypointID].getKv(NAME).replace('"', '')
            #comment = name + '<routespeed>' + str(pathInfoDict[waypointID][SPEED]) + '</routespeed>'
            comment = name
        else :
            #set coordinate from orig. airfield
            airfield = findObjectInRange(mission, planelist[0], Range=1000, Type=AIRFIELD)
            for info in [XPOS, YPOS, ZPOS]:
                newIcon.setKv(info, mission.ObjList[airfield[0]].getKv(info))
            name = mission.ObjList[airfield[0]].getKv(NAME).replace('"', '').replace('Fake ', '')
            comment = name + ' Takeoff'

        # set line type
        newIcon.setKv(LINETYPE, PATHLINESTYLE)
        newIcon.setKv(RCOLOR, PWCGsettings['flightColors'][flightNum][0])
        newIcon.setKv(GCOLOR, PWCGsettings['flightColors'][flightNum][1])
        newIcon.setKv(BCOLOR, PWCGsettings['flightColors'][flightNum][2])
        #add target
        newIcon.PropList['Targets'] = {iconNum+1}

        #add object in mission
        mission.addObject(newIcon, 0)
        #num = num +1
        # create associated langage entries
        lastlabelNo = max(mission.LabelsList.keys())
        lastlabelNoName = lastlabelNo + 1
        newIcon.setKv(LCNAME, lastlabelNoName)
        lastlabelNoComment = lastlabelNo + 2
        newIcon.setKv(LCDESC, lastlabelNoComment)
        mission.LabelsList[lastlabelNoName] = name
        mission.LabelsList[lastlabelNoComment] = comment

        # link to existing target Icon if TARGETKEYWORD
        if name == TARGETKEYWORD.replace('\"', ''):
            # find nearest action icon
            targetICONList = findObjectInRange(mission, iconNum, Range=10000, Type=MCUICON, IconId=ACTIONICONID)
            #change target to original target ICON
            mission.ObjList[iconNum].PropList['Targets'] = {targetICONList[0]}
            #change associated name and comment
            lastlabelNo = max(mission.LabelsList.keys())
            lastlabelNoName = lastlabelNo + 1
            mission.LabelsList[lastlabelNoName] = TARGETICONNAME
            mission.ObjList[targetICONList[0]].PropList[LCNAME]=lastlabelNoName
            lastlabelNoComment = lastlabelNo + 2
            # find target objective in comments
            for key in mission.LabelsList:
                if groupName.strip() in mission.LabelsList[key].strip()  and key > 5:
                    comment=mission.LabelsList[key+1]
            nameID =  mission.ObjList[targetICONList[0]].PropList[LCNAME]
            name = mission.LabelsList[nameID]
            createComment(mission, targetICONList[0], name, comment)

            mission.ObjList[targetICONList[0]].PropList['Coalitions'] = {0, 1, 2, 3, 4};

            # change target of target icon to next icon
            mission.ObjList[targetICONList[0]].PropList['Targets'] = {iconNum+1}


    #add last branch to airfield again
    # create WP icon
    iconNum = mission.MaxIndex + 1
    newIcon = templateMission.ObjList[templateIcon[0]].clone(iconNum)
    if groupName in escortInfoList:
        # set coordinate from the land MCU of the group
        airfield = findObject(mission, Type=MCULAND, Group=groupName)
    else:
        # set coordinate from orig. airfield
        airfield = findObjectInRange(mission, planelist[0], Range=1000, Type=AIRFIELD)

    for info in [XPOS, YPOS, ZPOS]:
        newIcon.setKv(info, mission.ObjList[airfield[0]].getKv(info))
    name = mission.ObjList[airfield[0]].getKv(NAME).replace('"', '').replace('Fake ', '')

    # set line type
    newIcon.setKv(LINETYPE, PATHLINESTYLE)

    newIcon.setKv(RCOLOR, PWCGsettings['flightColors'][flightNum][0])
    newIcon.setKv(GCOLOR, PWCGsettings['flightColors'][flightNum][1])
    newIcon.setKv(BCOLOR, PWCGsettings['flightColors'][flightNum][2])
    # notarget
    newIcon.PropList['Targets'] = set()
    # add object in mission
    mission.addObject(newIcon, 0)
    # create associated langage entries
    lastlabelNo = max(mission.LabelsList.keys())
    lastlabelNoName = lastlabelNo + 1
    newIcon.setKv(LCNAME, lastlabelNoName)
    lastlabelNoComment = lastlabelNo + 2
    newIcon.setKv(LCDESC, lastlabelNoComment)
    mission.LabelsList[lastlabelNoName] = name
    mission.LabelsList[lastlabelNoComment] = name + ' Land'

    #--------------------------------------------------------------------------------
    # create icon for starting point if not airstart
    if not airstart:
        #startTriggerName = groupName.replace('\"','').replace('Flight ','')+CTRIGGERTAKEOFF
        startTriggerName = groupName+CTRIGGERTAKEOFF
        Ctrigger = findObject(mission, Type=MCUCTRIGGER, Name = startTriggerName )
        #Ctrigger = findObject(mission, Type=MCUCTRIGGER)

        #add group icons
        iconNum = mission.MaxIndex + 1
        newIcon = templateMission.ObjList[templateIcon[0]].clone(iconNum)
        for info in [XPOS, YPOS, ZPOS]:
            newIcon.setKv(info, mission.ObjList[Ctrigger[0]].getKv(info))

        newIcon.setKv(ICONID, ACTIONICONID)
        newIcon.setKv(RCOLOR, 0)
        newIcon.setKv(GCOLOR, 0)
        newIcon.setKv(BCOLOR, 0)
        #ad assoicated name and comment
        createComment(mission, newIcon, STARTALLNAME, STARTALLCOMMENT)

        # add object in mission
        mission.addObject(newIcon, 0)

# ------------------------------------------------------------------------------------------------------------------------
def changeMissionComment(mission, planelist: list, groupList:list, escortInfoList:list, PWCGsettings:list):
    """ update mission comment """

    #mission comment = line 1 of LabelList
    originalMissionLabel = mission.LabelsList[1]
    originalMissionLabelSplit = originalMissionLabel.split('<br>')
    missionDate = originalMissionLabelSplit[2]

    #find map name by splitting GuiMap by '-' of mission obj 0
    mapName = (mission.ObjList[0].getKv(GUIMAP).split('-'))[0]

    groupPlaneModel = dict()
    mainGroups = dict()

    #find infos for plane groups
    for groupName in groupList:
        #find plane model
        groupPlaneList = findObject(mission, Type=PLANE, Group=groupName)
        planeModel = mission.ObjList[groupPlaneList[0]].getKv(SCRIPT).replace('\"LuaScripts\\WorldObjects\\Planes\\','').replace('.txt\"','')
        groupPlaneModel[groupName]=planeModel
        groupCommentID = -1
        # find objectif in mission comment
        if groupName not in escortInfoList:
            for ID in mission.LabelsList.keys():
                if groupName.strip() in mission.LabelsList[ID] and ID > 5:
                    groupCommentID = ID+1
            mainGroups[groupName] = groupCommentID


    #define new mission text
    newMissionText = mapName+' '+missionDate+'<br>'
    for groupName in groupList:
        if groupName not in escortInfoList:
            if mainGroups[groupName] in mission.LabelsList.keys():
                groupObjList = mission.LabelsList[mainGroups[groupName]].split('<br>')
                newMissionText = newMissionText + groupPlaneModel[groupName]+' of '+groupName+": "+ groupObjList[0]
                # find if escorted
                for escortGroup in escortInfoList:
                    if groupName == escortInfoList[escortGroup]:
                        newMissionText = newMissionText + " escorted by " + groupPlaneModel[
                            escortGroup] + " of " + escortGroup
            else:
                #put original mission text
                newMissionText = newMissionText + originalMissionLabelSplit[1] + '<br>' + originalMissionLabelSplit[3]

        newMissionText = newMissionText +'<br>'

    for escortGroup in escortInfoList:
        newMissionText = newMissionText + groupPlaneModel[escortGroup]+" of "+escortGroup+": escort "+groupPlaneModel[escortInfoList[escortGroup]]+" of "+escortInfoList[escortGroup] + '<br>'

    newMissionText = newMissionText+PWCGsettings['MissionHelpText']+"\n"
    newMissionText = newMissionText.replace('\"','').replace('\n','')

    #overwrite original mission text
    mission.LabelsList[1] = newMissionText
    mission.LabelsList[2] = mission.LabelsList[2].replace('\n','')+' and  Pyl2GB MiMec\n'

    #Change coalition of all icons
    flightIconList = findObject(mission, Type=MCUICON)
    set_kv(mission, flightIconList, Coalitions = {0, 1, 2, 3, 4} )


# ------------------------------------------------------------------------------------------------------------------------
def reduceGroupName(groupName:str) -> str:
    """ remove 'flight' in group name but keep way to differenciate groups """

    newName = groupName.replace('"', '').replace('Flight', '')

    return newName