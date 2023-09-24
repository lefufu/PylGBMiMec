from basic_functions.find_object import findObject, findObjectInRange
from basic_functions.mission_class import Mission
from basic_functions.modify_object import set_kv, get_kv, set_as_targetList, add_in_targetList, \
    add_OnEvents
from basic_functions.object_creation import copy_from_mission
from basic_functions.properties_class import Properties
from declarations.properties_specials import AIRFIELD, XPOS, ZPOS, YPOS, MCUWAYPOINT, NAME, YORI, COUNTRY, LINKTRID, \
    MISOBJID, MCUTIMER, MCUBEHAVIOUR, STARTINAIR, MCUMISSION, MCUENDMISSION, TIME, VEHICLE
from declarations.template_declaration import TEMPLATEAIRFIELD, TEMPLATETIMER, TEMPLATEBEHAVIOUR, TAKEOFFNAME, TOTALDISTANCE, \
    TARGETSTATUS, AIRSTARTNAME, TEMPLATEMENUAIRFIELD, TEMPLATEMENUMISSION, MENUMISSIONMCUNAME, TEMPLATEENDMISSION, \
    CANVASNAME, TAKEOFFWAYPTNAME, SETCOUNTRY, DEACTIVNAME, ACTIVNAME
import math

lastX = -1
lastY = -1
lastZ = -1
lastgroup = ''

# ---------------------------------------------
def createAirfields(mission:Mission, planelist: list, groupName : str, PWCGsettings : dict ,templateMission:Mission, pathInfoDict:dict, escortInfoList:dict):
    """ create the airfields and their activation logic for the selected flight """

    airFieldList = list()
    # define airplane model list

    waypointList = findObject(mission, Type=MCUWAYPOINT, Group=groupName)
    prevWaypoint=waypointList[0]

    #create start airfield by putting an empty waypoint list
    origAirfield = createSingleAirfield(mission, planelist, groupName, -1, PWCGsettings, 0, templateMission, pathInfoDict, prevWaypoint, escortInfoList)

    #create airfield for each waypoint (except target)
    waypointList = findObject(mission, Type=MCUWAYPOINT, Group=groupName)
    waypointList = sorted(waypointList)

    for waypoint in waypointList:
        newAirfield = createSingleAirfield(mission, planelist, groupName, waypoint, PWCGsettings, 0, templateMission,  pathInfoDict, prevWaypoint, escortInfoList)
        prevWaypoint = waypoint

        #avoid un needed airfields: will not work to optimize fuel !
        # if newAirfield != -1 :
        #     checkAirfield = findObjectInRange(mission, newAirfield, Range=int(PWCGsettings['cleanUPDistance']), Type=AIRFIELD, Name = groupName.replace('"','')+'_rejoin')
        #     if len(checkAirfield) > 1:
        #             for obj in range(1, len(checkAirfield)):
        #                 deleteObject(mission, checkAirfield[1:])

# ---------------------------------------------
def createSingleAirfield(mission: Mission, planelist: list, groupName: str, wayPoint:int , PWCGsettings : dict, intermediate : int,templateMission:Mission,  pathInfoDict:dict, prevWaypoint:int, escortInfoList:dict):
    """ create the airfields and their activation logic for the selected flight """

    airFieldNum=-1
    numberToAdd = 0
    airstart = 0

    #to compute distance from last WP
    global lastX, lastY, lastZ, lastgroup

    if (mission.ObjList[planelist[len(planelist)-1]]).PropList[STARTINAIR] == 0 :
        airstart = 1

    if (lastgroup != groupName):
        lastgroup = groupName
        lastX = -1
        lastY = -1
        lastZ = -1

    #handle takeoff airfield (no waypoint)
    if wayPoint != -1:
        waypointName = mission.ObjList[wayPoint].PropList[NAME]
        posX = mission.ObjList[wayPoint].PropList[XPOS]
        posY = mission.ObjList[wayPoint].PropList[YPOS]
        posZ = mission.ObjList[wayPoint].PropList[ZPOS]
    else:
        waypointName = ''
        posX = 0
        posY = 0
        posZ = 0

    skipFlag = 0

    #do not generate an airfield on target !
    if waypointName == 'Target Final':
        skipFlag = 1

    if wayPoint == -1 and airstart :
            skipFlag = 0

    distanceFromPrevious = pathInfoDict[wayPoint]['localDistance']

    # do not generate airfield if too near
    if distanceFromPrevious < PWCGsettings['minDistance'] and wayPoint != -1 and waypointName != '"TakeOff"':
        skipFlag = 1

    #generate additional airfield if too far
    if distanceFromPrevious > PWCGsettings['maxDistance'] and intermediate == 0 and waypointName != '"TakeOff"':
        numberToAdd = distanceFromPrevious//PWCGsettings['maxDistance']
        for intermediateNumber in range(int(numberToAdd)):
            createSingleAirfield(mission, planelist, groupName, wayPoint, PWCGsettings, numberToAdd,templateMission, pathInfoDict, prevWaypoint, escortInfoList )

    if skipFlag == 0:
        #airFieldName = waypointName.replace('"','')
        airFieldName = groupName+"_rejoin"

        #takeoff waypoint is in fact initial climb : 2 waypoints are to be created
        if wayPoint == -1:
            if not airstart:
                #create parking airfield
                # find nearest airfield
                airfield = findObjectInRange(mission, planelist[0], Range=1000, Type=AIRFIELD)
                name=mission.ObjList[airfield[0]]

                # get parking POS (first 'Chart' object and type=0)
                if ('Chart') in mission.ObjList[airfield[0]].PropList:
                    # Arfield has a chart declared => parking is used
                    airfieldParkingPoint = mission.ObjList[airfield[0]].PropList['Chart'][0]
                    parkingX = airfieldParkingPoint.Value['X']
                    parkingY = airfieldParkingPoint.Value['Y']
                    distance = math.sqrt(parkingX * parkingX + parkingY * parkingY)
                    cos = math.cos(math.radians(mission.ObjList[airfield[0]].PropList[YORI]))
                    sin = math.sin(math.radians(mission.ObjList[airfield[0]].PropList[YORI]))

                    spawnAirfieldX = mission.ObjList[airfield[0]].PropList[XPOS] + parkingX * cos - parkingY * sin
                    spawnAirfieldY = mission.ObjList[airfield[0]].PropList[YPOS]
                    spawnAirfieldZ = mission.ObjList[airfield[0]].PropList[ZPOS] + parkingX * sin + parkingY * cos
                    # temp = parkingX/distance
                    angle = mission.ObjList[airfield[0]].PropList[YORI]
                    if parkingY < 0:
                        angle = mission.ObjList[airfield[0]].PropList[YORI] + 90
                    else:
                        angle = mission.ObjList[airfield[0]].PropList[YORI] - 90
                else:
                    # no chart declared => used canvas as starting point
                    canvasList = findObjectInRange(mission, planelist[0], Range=1000, Type=VEHICLE, Name=CANVASNAME)
                    spawnAirfieldX = mission.ObjList[canvasList[0]].PropList[XPOS]
                    spawnAirfieldY = mission.ObjList[canvasList[0]].PropList[YPOS]
                    spawnAirfieldZ = mission.ObjList[canvasList[0]].PropList[ZPOS]
                    deltaX = mission.ObjList[planelist[0]].PropList[XPOS] - spawnAirfieldX
                    deltaZ = mission.ObjList[planelist[0]].PropList[ZPOS] - spawnAirfieldZ
                    # not working (should point to plane but will make plane taking off in wrong direction)
                    #angle = math.degrees(math.atan(deltaZ/deltaX))
                    angle = mission.ObjList[planelist[0]].PropList[YORI]

                #set parking with or without engine
                if PWCGsettings['EngineOffOnStart'] :
                    StartInAir = 2
                else :
                    StartInAir = 1
                airFieldName = groupName + TAKEOFFNAME
                country = mission.ObjList[planelist[0]].getKv('Country')
            else:
                # create airstart airfield
                # use last plane coordinate and orientation for waypoint
                spawnAirfieldX = mission.ObjList[planelist[ len(planelist)-1 ]].PropList[XPOS]
                spawnAirfieldY = mission.ObjList[planelist[ len(planelist)-1 ]].PropList[YPOS]
                spawnAirfieldZ = mission.ObjList[planelist[ len(planelist)-1 ]].PropList[ZPOS]
                angle = mission.ObjList[planelist[len(planelist)- 1]].PropList[YORI]
                #set airstart
                StartInAir = 0
                airFieldName = groupName + AIRSTARTNAME
                country = mission.ObjList[planelist[0]].getKv('Country')

        else:
            spawnAirfieldX = posX+PWCGsettings['DeltaX']
            spawnAirfieldY = posY+PWCGsettings['altitudeAboveWaypoint']
            spawnAirfieldZ = posZ
            angle = mission.ObjList[wayPoint].PropList[YORI]
            #TODO to check
            StartInAir = 0
            country=0
            #handle additional waypoints
            if intermediate != 0 :
                deltaX = (posX-mission.ObjList[prevWaypoint].PropList[XPOS])/(intermediate+1)
                deltaY = (posY-mission.ObjList[prevWaypoint].PropList[YPOS])/(intermediate+1)
                deltaZ = (posZ-mission.ObjList[prevWaypoint].PropList[ZPOS])/(intermediate+1)
                spawnAirfieldX = deltaX + lastX
                spawnAirfieldY = deltaY + lastY + PWCGsettings['altitudeAboveWaypoint']
                spawnAirfieldZ = deltaZ + lastZ
                airFieldName = airFieldName+'#'+str(intermediate)

        #create airfield from template airfield
        templateAirfield = findObject(templateMission, Type=AIRFIELD, Name = TEMPLATEAIRFIELD)
        airFieldNum = mission.MaxIndex + 1
        linkIDNum = airFieldNum + 1
        newAirfield = templateMission.ObjList[templateAirfield[0]].clone(airFieldNum)
        #------------------------------------------------------
        #for each plane create a planeset
        newProplist = list()

        for plane in range(len(planelist)):
            #go reverse to get plane to replace
            revPlane = len(planelist)-plane -1

            #create associated property
            newPlaneSetProp = Properties('')
            newPlaneSetProp.Value = dict()
            #copy key values from the template
            newPlaneSetProp = templateMission.ObjList[templateAirfield[0]].PropList['Planes'][0].Value.copy()
            #modify it accordingly to plane
            newPlaneSetProp['Model'] = mission.ObjList[planelist[revPlane]].getKv('Model')
            newPlaneSetProp['Script'] = mission.ObjList[planelist[revPlane]].getKv('Script')
            newPlaneSetProp['Name'] = mission.ObjList[planelist[revPlane]].getKv('Name')
            newPlaneSetProp['TCode'] = mission.ObjList[planelist[revPlane]].getKv('TCode')
            newPlaneSetProp['TCodeColors'] = mission.ObjList[planelist[revPlane]].getKv('TCodeColor')
            newPlaneSetProp['Skin'] = mission.ObjList[planelist[revPlane]].getKv('Skin')
            fuel = mission.ObjList[planelist[revPlane]].getKv('Fuel')
            if 'Name' in pathInfoDict.keys() :
                if pathInfoDict[wayPoint]['Name'] != TAKEOFFWAYPTNAME:
                    ratio = pathInfoDict[wayPoint][TOTALDISTANCE] / pathInfoDict[-1][TOTALDISTANCE]
                    fuel = (mission.ObjList[planelist[revPlane]].getKv('Fuel'))-ratio*(mission.ObjList[planelist[revPlane]].getKv('Fuel')*(1-PWCGsettings['fuelMargin']))
            newPlaneSetProp['Fuel'] = fuel
            newPlaneSetProp['Callsign'] = mission.ObjList[planelist[revPlane]].getKv('Callsign')
            newPlaneSetProp['Callnum'] = mission.ObjList[planelist[revPlane]].getKv('Callnum')
            newPlaneSetProp['AILevel'] = mission.ObjList[planelist[revPlane]].getKv('AILevel')
            # todo fix limit mod and payload
            #setup payload to player plane (should be empty) if waypoint is after target
            if pathInfoDict[wayPoint][TARGETSTATUS] == 1:
                 newPlaneSetProp['PayloadId'] = mission.ObjList[planelist[len(planelist) - 1]].getKv('PayloadId')
                 newPlaneSetProp['WMMask'] = mission.ObjList[planelist[len(planelist) - 1]].getKv('WMMask')
            else:
                 newPlaneSetProp['PayloadId'] = mission.ObjList[planelist[0]].getKv('PayloadId')
                 newPlaneSetProp['WMMask'] = mission.ObjList[planelist[0]].getKv('WMMask')

            #newPlaneSetProp['PayloadId'] = mission.ObjList[planelist[0]].getKv('PayloadId')
            #newPlaneSetProp['WMMask'] = mission.ObjList[planelist[revPlane]].getKv('WMMask')



            newPlaneSetProp['Number'] = 1
            # number of replacement (no default planeset)
            newPlaneSetProp['SetIndex'] = plane
            # depend of airfield
            newPlaneSetProp['StartInAir'] = StartInAir
            newPlaneSetProp['Altitude'] = spawnAirfieldY

            #add it to the property list
            prop = Properties(newPlaneSetProp)

            newProplist.append(prop)
        #modify the airfield to use the list
        newAirfield.PropList['Planes'] = newProplist

        # ------------------------------------------------------
        #set position and other elements
        newAirfield.setKv(XPOS,spawnAirfieldX )
        newAirfield.setKv(YPOS,spawnAirfieldY )
        newAirfield.setKv(ZPOS,spawnAirfieldZ )
        newAirfield.setKv(NAME, airFieldName)
        #newAirfield.setKv(NAME,waypointName.replace('"','') )
        newAirfield.setKv(YORI, angle)
        newAirfield.setKv(LINKTRID,linkIDNum)
        lastX = spawnAirfieldX
        lastY = spawnAirfieldY
        lastZ = spawnAirfieldZ

        #  country set to neutral by default or by plane country for the takeoff
        newAirfield.setKv(COUNTRY, country)

        #------------------------------------------------------
        # if parking airfield having chart, modify it to take into account rotation and translation to parking
        if wayPoint == -1 and airstart == 0  and ('Chart' in mission.ObjList[airfield[0]].PropList) :
            origchart =  mission.ObjList[airfield[0]].PropList['Chart']
            newChart = origchart.copy()
            if parkingY < 0:
                angle=90

            else :
                angle = -90
            cos = math.cos(math.radians(angle))
            sin = math.sin(math.radians(angle))
            for point in newChart:
                origX= point.Value['X']
                origY = point.Value['Y']
                newX = origX * cos + origY * sin
                newY = -origX * sin + origY * cos
                deltaX = parkingX * cos + parkingY * sin
                deltaY = -parkingX * sin + parkingY * cos
                point.Value['X'] = newX - deltaX
                point.Value['Y'] = newY - deltaY

            newAirfield.PropList['Chart'] = newChart


        # ------------------------------------------------------
        #add airfield & linkID
        mission.addObject(newAirfield, 0)

        #create associated linkID
        linkIDTemplate = findObject(templateMission, Type='MCU_TR_Entity')
        newlinkID = templateMission.ObjList[linkIDTemplate[0]].clone(linkIDNum)

        newlinkID.setKv(XPOS,spawnAirfieldX)
        newlinkID.setKv(YPOS,spawnAirfieldY)
        newlinkID.setKv(ZPOS,spawnAirfieldZ)
        newlinkID.setKv(NAME, '')
        newlinkID.setKv(MISOBJID, airFieldNum)
        mission.addObject(newlinkID, 0)


    return airFieldNum


# -------------------------------------------------------------------------------
def createMenuAirfield(mission, PWCGsettings:list, templateMission, planelist):
    """ create menu airfield to abort mission and go to menu server"""

    posX = mission.Xmax-PWCGsettings['DeltaX']*100
    deltaZ = 100
    #create 'end mission' MCU
    templateEndMissionList = findObject(templateMission, Type=MCUENDMISSION, Name=TEMPLATEENDMISSION)
    missionEndNum = mission.MaxIndex + 1
    endMissionEndMCU = templateMission.ObjList[templateEndMissionList[0]].clone(missionEndNum)
    endMissionEndMCU.setKv(XPOS, posX+PWCGsettings['DeltaX'])
    endMissionEndMCU.setKv(ZPOS, mission.Zmin+PWCGsettings['DeltaZ']*deltaZ)
    endMissionEndMCU.setKv(NAME, MENUMISSIONMCUNAME)
    mission.addObject(endMissionEndMCU, 0)

    # ------------------------------------------
    # create the timer to call mission end
    templateTimer = findObject(templateMission, Type=MCUTIMER, Name=TEMPLATETIMER)
    endTimerNum = mission.MaxIndex + 1
    newEndTimer = templateMission.ObjList[templateTimer[0]].clone(endTimerNum)
    # Timer
    newEndTimer.setKv(XPOS, posX+PWCGsettings['DeltaX'])
    newEndTimer.setKv(ZPOS, mission.Zmin+PWCGsettings['DeltaZ']*(deltaZ-1))
    newEndTimer.setKv(TIME, 1.0)
    newEndTimer.setKv(NAME, MENUMISSIONMCUNAME)
    # target = next mission MCU
    newEndTimer.PropList['Targets'] = set()
    newEndTimer.PropList['Targets'].add(missionEndNum)
    mission.addObject(newEndTimer, 0)

    #create 'next mission' MCU
    templateMenuMissionList = findObject(templateMission, Type=MCUMISSION, Name=TEMPLATEMENUMISSION)
    missionMCUNum = mission.MaxIndex + 1
    newMissionMCU = templateMission.ObjList[templateMenuMissionList[0]].clone(missionMCUNum)
    newMissionMCU.setKv(XPOS, posX)
    newMissionMCU.setKv(ZPOS, mission.Zmin+PWCGsettings['DeltaZ']*(deltaZ-1))
    newMissionMCU.setKv(NAME, MENUMISSIONMCUNAME)
    mission.addObject(newMissionMCU, 0)

    # create the timer to call by the spawn
    templateTimer = findObject(templateMission, Type=MCUTIMER, Name=TEMPLATETIMER)
    timerNum = mission.MaxIndex + 1
    newTimer = templateMission.ObjList[templateTimer[0]].clone(timerNum)
    # Timer
    newTimer.setKv(XPOS, posX)
    newTimer.setKv(ZPOS, mission.Zmin+PWCGsettings['DeltaZ']*(deltaZ-2))
    newTimer.setKv(NAME, MENUMISSIONMCUNAME)
    newTimer.setKv(TIME, 1.0)
    # target = next mission MCU
    newTimer.PropList['Targets'] = set()
    newTimer.PropList['Targets'].add(missionMCUNum)
    newTimer.PropList['Targets'].add(endTimerNum)
    mission.addObject(newTimer, 0)

    #get template airfield
    templateMenuAirfieldList = findObject(templateMission, Type=AIRFIELD, Name=TEMPLATEMENUAIRFIELD)
    airFieldNum = mission.MaxIndex + 1
    templateMenuAirfield = templateMission.ObjList[templateMenuAirfieldList[0]]
    templateLinkID = templateMenuAirfield.PropList[LINKTRID]
    linkIDNum = airFieldNum+1
    newAirfield = templateMenuAirfield.clone(airFieldNum)
    newlinkID = templateMission.ObjList[templateLinkID].clone(linkIDNum)

    #update new airfield
    posXAirfield=posX
    posZAirfield = mission.Zmin+PWCGsettings['DeltaZ']*(deltaZ-3)
    newAirfield.setKv(XPOS, posXAirfield)
    newAirfield.setKv(ZPOS, posZAirfield)
    newAirfield.setKv(NAME, PWCGsettings['MenuAirfieldName'])
    newAirfield.setKv(LINKTRID, linkIDNum)
    country = mission.ObjList[planelist[0]].getKv(COUNTRY)
    newAirfield.setKv(COUNTRY, country)
    mission.addObject(newAirfield, 0)

    newlinkID.setKv(XPOS, posX)
    newlinkID.setKv(ZPOS, mission.Zmin+PWCGsettings['DeltaZ']*(deltaZ-3))
    newlinkID.setKv(NAME, PWCGsettings['MenuAirfieldName'])
    newlinkID.setKv(MISOBJID, airFieldNum)

    #point to the timer
    newlinkID.PropList['OnEvents'][0].Value['TarId']=timerNum

    mission.addObject(newlinkID, 0)

    # ------------------------------------------
    # add enable/disable mecanism
    disableAirfield = copy_from_mission(mission, templateMission, Type=MCUBEHAVIOUR, Name=TEMPLATEBEHAVIOUR)
    # set country to neutral
    set_kv(mission, disableAirfield, XPos=posXAirfield, ZPos=posZAirfield-PWCGsettings['DeltaZ'], FloatParam=0, Filter=SETCOUNTRY, Name=MENUMISSIONMCUNAME+DEACTIVNAME )
    set_as_targetList(mission, disableAirfield, airFieldNum)

    EnableAirfield = copy_from_mission(mission, templateMission, Type=MCUBEHAVIOUR, Name=TEMPLATEBEHAVIOUR)
    # set country to player country
    country = get_kv(mission, planelist, COUNTRY )
    set_kv(mission, EnableAirfield, XPos=posXAirfield-PWCGsettings['DeltaX'], ZPos=posZAirfield-PWCGsettings['DeltaZ'], FloatParam=0, Country=country, Filter=SETCOUNTRY,Name=MENUMISSIONMCUNAME+ACTIVNAME )
    set_as_targetList(mission, EnableAirfield, airFieldNum)

    #Add timers
    enable_timer = copy_from_mission(mission, templateMission, Type=MCUTIMER, Name=TEMPLATETIMER)
    set_kv(mission, enable_timer, XPos=posXAirfield-PWCGsettings['DeltaX'], ZPos=posZAirfield - PWCGsettings['DeltaZ']*2, Name=MENUMISSIONMCUNAME + ACTIVNAME, Time=PWCGsettings['MenuAirfieldTimeout'])
    set_as_targetList(mission, enable_timer, EnableAirfield)

    disable_timer = copy_from_mission(mission, templateMission, Type=MCUTIMER, Name=TEMPLATETIMER)
    set_kv(mission, disable_timer, XPos=posXAirfield, ZPos=posZAirfield - PWCGsettings['DeltaZ'] * 2,
           Name=MENUMISSIONMCUNAME + DEACTIVNAME, Time=1.0)
    set_as_targetList(mission, disable_timer, disableAirfield)
    add_in_targetList(mission, disable_timer, enable_timer)

    # Add deactivate timer for every respawn
    airfieldList=findObject(mission, Type=AIRFIELD)
    add_OnEvents(mission, airfieldList, 'OnPlaneSpawned', disable_timer)


    return