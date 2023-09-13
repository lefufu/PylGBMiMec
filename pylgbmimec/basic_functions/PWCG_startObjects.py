from basic_functions.find_object import findObject, findObjectInRange
from basic_functions.mission_class import Mission
from basic_functions.modify_object import deleteObject, add_in_targetList, add_OnEvents, set_kv, set_subtitleValues, \
    add_in_objectList, set_as_targetList, get_kv
from basic_functions.object_creation import copy_from_mission
from basic_functions.properties_class import Properties
from declarations.properties_specials import XPOS, ZPOS, LINKTRID, \
    MCUCOUNTER, MCUTIMER, MCUDELETE, MCUBEHAVIOUR, AIRFIELD, MCUTR, MCUWAYPOINT, MCUCTRIGGER, YPOS, COUNTRY, TIME, \
    ENABLED, MCUDEACTIVATE, MCUACTIVATE, EVENTENTER, MCUBEGIN, MCUTAKEOFF, STARTINAIR, PLANE, NAME, EFFECT, MCUSUBTITLE, \
    MCUCMDEFFECT, MCUMISSIONBEGIN, TARGETS
from declarations.template_declaration import TEMPLATECOUNTER, TEMPLATETIMER, TEMPLATEDELETE, \
    TEMPLATEBEHAVIOUR, COUNTERNAME, TIMERNAME, DELETENAME, BEHAVIOURNAME, SETPLANESET, TEMPLATEAIRFIELD, TRNAME, \
    SETONSPAWN, BEHDEACTALL, SETCOUNTRY, TEMPLATECTRIGGER, CTRIGGERNAME, BEHAVAFNAME, AFTIMERNAME, TEMPLATEDEACTIVATE, \
    DEACTIVATENAME, TEMPLATEACTIVATE, ACTIVATENAME, GLOBALCOUNTERNAME, STARTALLNAME, TAKEOFFCOMMAND, AIRSTART, \
    AIRSTARTNAME, AIRSTARTFORCETAKEOFF, SIGNALNAME, TAKEOFFNAME, ACTIVNAME, DEACTIVNAME, CTRIGGERTAKEOFF, \
    TEMPLATESUBTITLE, TEMPLATEBEGIN, BEGINNAME, LAUNCHNAME, GOTONAME


def createStartLogicAll(mission: Mission, planelist: list, groupList: list, airfieldList : list, PWCGsettings: dict, templateMission:Mission, startTrigger:list, escortInfoList:dict):
    """ create the logic for airfield activation for the selected flight """

    # ----------------------------
    #  get informations

    # find takeoff counter of each group
    takeoffSet=set()
    #begin of each group
    airfieldBeginDict = dict()
    #airstart of each group
    airstartDict = dict()
    #middle position for common objects (subtitle, start all counter,...)
    midX=0
    midZ=0

    for groupName in groupList:
        planelist =  findObject(mission, Type=PLANE, Group=groupName)
        if (mission.ObjList[planelist[len(planelist) - 1]]).PropList[STARTINAIR] == 0:
            airstartDict[groupName] = 1
            airstart = 1
        else:
            airstartDict[groupName] = 0
            airstart = 0

        if not(airstart) :
            takeOffCommandList = findObject(mission, Type=MCUTAKEOFF, Name=TAKEOFFCOMMAND, Group=groupName)
        else:
            takeOffCommandList = findObject(mission, Name=AIRSTART, Group=groupName)

        for ID in takeOffCommandList:
            takeoffSet.add(ID)

        # find mission begin of each group
        beginTempList = sorted(findObject(mission, Type=MCUBEGIN, Group=groupName))
        # find target timer pointed by the first mission begin
        targetTimer = mission.ObjList[beginTempList[0]].PropList['Targets']
        airfieldBeginDict[groupName] = targetTimer

        #middle position
        midX=midX+get_kv(mission, planelist[0], XPOS)
        midZ = midZ + get_kv(mission, planelist[0], ZPOS)

    midX = midX / len(groupList)
    midZ = midZ / len(groupList)

    # ---------------------------------------------------------------------------------
    # activate IA planes of players flight on first player spawn (whatever the flight)
    # if airstart : activate all flights, else only the player flight (takeoff will activate all)

    firstSpawnTargets = set()
    for groupName in groupList:
        #find 1st spawn timer
        firstSpawnTimer = findObject(mission, Type=MCUTIMER, Name=groupName+TIMERNAME+'1')
        if airstartDict[groupName] == 0:
            # ground start : only current flight begin is added to the timer target
            add_in_targetList(mission, firstSpawnTimer, airfieldBeginDict[groupName])
        else:
            # air start : all flight begin are added to the timer target
            for key in airfieldBeginDict:
                add_in_targetList(mission, firstSpawnTimer, airfieldBeginDict[key])

    # # find mission begin of each group
    # for groupName in groupList:
    #     beginList = set()
    #     # find group
    #     beginTempList=sorted(findObject(mission, Type=MCUBEGIN, Group=groupName))
    #     # find target timer pointed by the first mission begin
    #     targetTimer = mission.ObjList[beginTempList[0]].PropList['Targets']
    #     beginList.update(targetTimer)
    #     airfieldBeginDict[groupName]=targetTimer
    #     # remove mission begin target to avoid to process it later
    #     mission.ObjList[beginTempList[0]].PropList['Targets']=set()


    #add a new target for global counter  on timers for 1st spawn for ea
    # firstSpawnTimerList = findObject(mission, Type=MCUTIMER, Name=TIMERNAME+'1')
    # for timer in firstSpawnTimerList:
    #     newTargetSet=mission.ObjList[timer].PropList['Targets']
    #     newTargetSet.add(coutnerNum)
    #     mission.ObjList[timer].PropList['Targets']=newTargetSet

    startAllTargets = set()

    #build target list of all mission begin
    allBeginList = findObject(mission, Type=MCUBEGIN)

    for MCUbeginID in allBeginList:
        targetSet=mission.ObjList[MCUbeginID].PropList['Targets']
        startAllTargets.update(targetSet)
        #purge begin target to avoid an automatic start
        mission.ObjList[MCUbeginID].PropList['Targets']=set()

    #update start timer targets to replace mission begin
    # for timer in startALLTimerList:
    #     mission.ObjList[timer].PropList['Targets'] = startAllTargets

    #delete mission begin
    if PWCGsettings['Debug'] is not True:
        deleteObject(mission, allBeginList)

    # create a timer to trigger takeoff after starting all targets, additionalDelay contain the time beween activation and takeoff
    takeOffCommandList = findObject(mission, Type=MCUTAKEOFF, Name=TAKEOFFCOMMAND)
    takeoffTimer = copy_from_mission(mission, templateMission, Type=MCUTIMER, Name=TEMPLATETIMER)
    set_kv(mission, takeoffTimer, Name=STARTALLNAME+TAKEOFFNAME, XPos=midX+ PWCGsettings['DeltaX'], ZPos=midZ - PWCGsettings['DeltaZ'], Time=PWCGsettings['TakeOffTimerDelay'])
    set_as_targetList(mission, takeoffTimer, takeOffCommandList )

    # create 'start all' timers to replace mission begin, due to the high number of begin, multiple timer are created
    startAllTimerlist = list()
    cutrange = int(len(startAllTargets)/(PWCGsettings['StartAllTimerNB']))
    for timerNo in range(2, PWCGsettings['StartAllTimerNB']+1):
        startALLTimer = copy_from_mission(mission, templateMission, Type=MCUTIMER, Name=TEMPLATETIMER)
        set_kv(mission, startALLTimer, Name=STARTALLNAME+str(timerNo), XPos=midX+ PWCGsettings['DeltaX']*timerNo, ZPos=midZ+ PWCGsettings['DeltaZ'], Time=PWCGsettings['DeactTimerDelay'] )
        for i in range(1,cutrange):
            tmpTargetID = startAllTargets.pop()
            add_in_targetList(mission, startALLTimer, tmpTargetID )
        #startAllTimerlist.append(startALLTimer)
        startAllTimerlist = startAllTimerlist + startALLTimer

    #add the last timer with the remaining startAllTargets
    startALLTimer = copy_from_mission(mission, templateMission, Type=MCUTIMER, Name=TEMPLATETIMER)
    set_kv(mission, startALLTimer, Name=STARTALLNAME + '1', XPos=midX + PWCGsettings['DeltaX'] , ZPos=midZ + PWCGsettings['DeltaZ'], Time=PWCGsettings['DeactTimerDelay'])
    set_as_targetList(mission, startALLTimer, startAllTargets)
    #startAllTimerlist.append(startAllTargets)
    startAllTimerlist = startAllTimerlist + startALLTimer

    # create a counter to avoid to call multiple time start on
    startALLCounter = copy_from_mission(mission, templateMission, Type=MCUCOUNTER, Name=TEMPLATECOUNTER)
    set_kv(mission, startALLCounter, Name=GLOBALCOUNTERNAME, XPos=midX+PWCGsettings['DeltaX']*(PWCGsettings['StartAllTimerNB']/2),
           ZPos=midZ - PWCGsettings['DeltaZ']*2, Counter=1)
    set_as_targetList(mission, startALLCounter, takeoffTimer)
    add_in_targetList(mission, startALLCounter, startAllTimerlist)

    # affect counter to complex trigger takeoff target
    groundStartTriggerList = findObject(mission, Type=MCUCTRIGGER, Name=CTRIGGERTAKEOFF)
    add_OnEvents(mission, groundStartTriggerList, 'OnObjectEnteredSimple', startALLCounter)

    # affect counter to airstart airfields
    airStartAirfieldsList = findObject(mission, Type=AIRFIELD, Name=AIRSTARTNAME)
    add_OnEvents(mission, airStartAirfieldsList, 'OnPlaneSpawned', startALLCounter)

    # ------------------------------------------------------------------------------
    # Add subttitle to explain player to go to mark
    startSubTitle = copy_from_mission(mission, templateMission, Type=MCUSUBTITLE, Name=TEMPLATESUBTITLE)
    #use last xPos, ZPos
    set_kv(mission, startSubTitle, XPos=midX,  ZPos=midZ, Name=GOTONAME)
    #HAlign : 0:Left/1:center/2:right
    #VALIGN : 0:Top, 1: center, 2:bottom
    set_subtitleValues(mission, startSubTitle, Duration=PWCGsettings['StartSubTitleDuration'], FontSize = PWCGsettings['StartSubTitleFontSize'],
                       Name=GOTONAME, HAlign = 1, VAlign = 0 , RColor=255, GColor=0, BColor=0, Text=PWCGsettings['StartSubTitleMessage'] )

    # display subtitle and no more start smoke
    #smokeListActivate = findObject(mission, Type=MCUCMDEFFECT,  Name=SIGNALNAME + ACTIVNAME)
    # create a timer
    startSbuTitleTimer = copy_from_mission(mission, templateMission, Type=MCUTIMER, Name=TEMPLATETIMER)
    set_kv(mission, startSbuTitleTimer, XPos=midX, ZPos=midZ, Time=5, Name=SIGNALNAME + ACTIVNAME)
    # set timer target to smoke activate and subtitle
    #set_as_targetList(mission, startSmokeTimer, smokeListActivate)
    add_in_targetList(mission, startSbuTitleTimer,startSubTitle)
    # add an event in airfield to trigger smoke and message (smoke not working because at zero height)
    airFieldList = findObject(mission, Type=AIRFIELD, Name=TAKEOFFNAME)
    add_OnEvents(mission, airFieldList, 'OnPlaneSpawned', startSbuTitleTimer)

    # ------------------------------------------------------------------------------
    # move canvas objects to show trigger zone
    #find ctriggers
    ctriggerList = findObject(mission, Type=MCUCTRIGGER, Name=CTRIGGERTAKEOFF)
    for triggerID in ctriggerList:
        Xpos = get_kv(mission, triggerID, 'XPos')
        Ypos = get_kv(mission, triggerID, 'YPos')
        Zpos = get_kv(mission, triggerID, 'ZPos')
        #get nearest canvas
        canvasList = findObjectInRange(mission, triggerID, 2000, Name='Canvas')
        deltaX = Xpos - get_kv(mission, canvasList[0], 'XPos')
        deltaZ = Zpos - get_kv(mission, canvasList[0], 'ZPos')
        for canvasID in canvasList:
            newXPos =  get_kv(mission, canvasID, 'XPos') + deltaX
            newZPos = get_kv(mission, canvasID, 'ZPos') + deltaZ
            set_kv(mission, canvasID, XPos=newXPos, ZPos=newZPos)

    # activate smoke at mission start because not working when triggered by timer ! (smoke not working because at zero height)
    # missionStartIDList = copy_from_mission(mission, templateMission, Type=MCUMISSIONBEGIN, Name=TEMPLATEBEGIN)
    # set_kv(mission, missionStartIDList, XPos=XPos, YPos=0, ZPos=ZPos, Name=groupName + SIGNALNAME + BEGINNAME)
    # set_as_targetList(mission, missionStartIDList, smokeListActivate)

    # de activate subtitle if enter the start zone (smoke not working because at zero height)
    # smokeListDeActivate = findObject(mission, Type=MCUCMDEFFECT,  Name=SIGNALNAME + DEACTIVNAME)
    # add_in_objectList(mission, smokeListDeActivate, startSubTitle)
    # ctriggerList = findObject(mission, Type=MCUCTRIGGER, Name=CTRIGGERTAKEOFF)
    # add_OnEvents(mission, ctriggerList, 'OnObjectEnteredSimple', smokeListDeActivate)

   # ------------------------------------------------------------------------------
    # Add subttitle to show mission start
    LaunchedSubTitle = copy_from_mission(mission, templateMission, Type=MCUSUBTITLE, Name=TEMPLATESUBTITLE)
    #use last xPos, ZPos
    set_kv(mission, LaunchedSubTitle, XPos=midX+PWCGsettings['DeltaX'],  ZPos=midZ, Name=LAUNCHNAME)
    #HAlign : 0:Left/1:center/2:right
    #VALIGN : 0:Top, 1: center, 2:bottom
    set_subtitleValues(mission, LaunchedSubTitle, Duration=PWCGsettings['StartSubTitleDuration'], FontSize = PWCGsettings['StartSubTitleFontSize'], HAlign = 1, VAlign = 1 , RColor=0, GColor=255, BColor=0, Text=PWCGsettings['LaunchedSubTitleMessage'] )
    add_in_targetList(mission, startALLTimer, LaunchedSubTitle)