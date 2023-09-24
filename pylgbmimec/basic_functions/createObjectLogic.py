from basic_functions.find_object import findObject
from basic_functions.mission_class import Mission
from basic_functions.properties_class import Properties
from declarations.properties_specials import XPOS, ZPOS, MCUTIMER, AIRFIELD, MCUCTRIGGER, YPOS, ENABLED, MCUDEACTIVATE, \
    MCUTAKEOFF, EVENTTOOKOFF
from declarations.template_declaration import TEMPLATECTRIGGER, TEMPLATEDEACTIVATE, \
    DEACTIVATENAME, TAKEOFFNAME, TAKEOFFCOMMAND, CTRIGGERTAKEOFF


def createstartFlightLogic(mission: Mission, planelist: list, groupName: str, airfieldList : list, PWCGsettings: dict, templateMission:Mission, escortInfoList):
    """ create the logic to start/activate all AI in mission """

    #add activation of all AI objects when reaching starting zone
    #find start airfield
    startAirfliedList = findObject(mission, Type=AIRFIELD, Name=groupName + TAKEOFFNAME)

    compTriggerNum = -1

    # ----------------------------------------
    #find trigger location (player plane)
    playerPlaneID = planelist[len(planelist)-1]
    XPos = mission.ObjList[playerPlaneID].getKv(XPOS)
    #player plane has an height of 0...
    YPos = mission.ObjList[playerPlaneID].getKv(YPOS)
    ZPos = mission.ObjList[playerPlaneID].getKv(ZPOS)

    # ----------------------------------------
    #modify  AI logic to remove takeoff command if not escort group (airstart)
    # TODO handle airstart ?
    if groupName not in escortInfoList.keys() :
        takeOffCommandList = findObject(mission, Type=MCUTAKEOFF, Name=TAKEOFFCOMMAND, Group = groupName)
        callingTimerList = findObject(mission, Type=MCUTIMER,  Group = groupName, Targets = takeOffCommandList[0])
        callingTimer  = callingTimerList[0]
        oldTargetList = mission.ObjList[callingTimer].getTarget()
        #remove takeoff from timer target
        oldTargetList.remove(takeOffCommandList[0])
        mission.ObjList[callingTimer].setTarget(oldTargetList)

        # ----------------------------------------
        # create timer to replace mission begin later
        #clone the timer
        # templateTimer = findObject(templateMission, Type=MCUTIMER, Name = TEMPLATETIMER)
        # timerNum = mission.MaxIndex + 1
        # newTimer = templateMission.ObjList[templateTimer[0]].clone(timerNum)
        # # Timer
        # newTimer.setKv('Name', groupName+STARTALLNAME)
        # newTimer.setKv('XPos', XPos + PWCGsettings['DeltaX'])
        # newTimer.setKv('ZPos', ZPos + PWCGsettings['DeltaX'])
        # newTimer.setKv('Time', PWCGsettings['DeactTimerDelay'])
        # #target
        # newTimer.PropList['Targets'] = set()
        # mission.addObject(newTimer, 0)

        # ----------------------------------------
        #create trigger to activate takeoff
        templateCompTrigger = findObject(templateMission, Type=MCUCTRIGGER, Name=TEMPLATECTRIGGER)
        compTriggerNum = mission.MaxIndex + 1
        newcompTrigger = templateMission.ObjList[templateCompTrigger[0]].clone(compTriggerNum)
        newcompTrigger.setKv('Name', groupName+ CTRIGGERTAKEOFF )
        newcompTrigger.setKv('Country', mission.ObjList[planelist[0]].getKv('Country'))
        newcompTrigger.setKv('Radius', PWCGsettings['takeoffRadius'])
        newcompTrigger.PropList['ObjectScript'] = [mission.ObjList[planelist[0]].getKv('Script')]

        newcompTrigger.setKv(XPOS, XPos)
        newcompTrigger.setKv(YPOS, YPos)
        newcompTrigger.setKv(ZPOS, ZPos)
        #add takeoff MCU for "enter" event
        newProplist = list()
        newEventSetProp = Properties('')
        newEventSetProp.Value = dict()
        # set takeoff when enter
        #newEventSetProp = templateMission.ObjList[templateCompTrigger[0]].PropList['OnEvents'][0].Value.copy()
        #newEventSetProp['Type'] = EVENTENTER
        #newEventSetProp['TarId'] = takeOffCommandList[0]
        #prop = Properties(newEventSetProp)
        #newProplist.append(prop)
        # disable when takeoff
        newEventSetProp = templateMission.ObjList[templateCompTrigger[0]].PropList['OnEvents'][0].Value.copy()
        newEventSetProp['Type'] = EVENTTOOKOFF
        newEventSetProp['TarId'] = compTriggerNum+1
        prop = Properties(newEventSetProp)
        newProplist.append(prop)
        # call a master timer when enter to replace mission start
        #TODO check
        # newEventSetProp = templateMission.ObjList[templateCompTrigger[0]].PropList['OnEvents'][0].Value.copy()
        # newEventSetProp['Type'] = EVENTENTER
        # newEventSetProp['TarId'] = timerNum
        # prop = Properties(newEventSetProp)
        # newProplist.append(prop)

        # modify the airfield to use the list
        newcompTrigger.PropList['OnEvents'] = newProplist
        # trigger is activated by default
        newcompTrigger.setKv(ENABLED, 1)
        mission.addObject(newcompTrigger, 0)

        # ----------------------------------------
        # create a smoke on trigger point and associated activate/deactivate => no way to get height !
        # smokeIDList = copy_from_mission(mission, templateMission, Type=EFFECT, Name=TEMPLATESIGNALNAME)
        # set_kv(mission, smokeIDList, XPos=XPos, YPos=YPos, ZPos=ZPos, Name=groupName + SIGNALNAME)
        # smokeIDactivList = copy_from_mission(mission, templateMission, Type=MCUCMDEFFECT, Name=TEMPLATECOMMAND)
        # set_kv(mission, smokeIDactivList, XPos=XPos, YPos=YPos, ZPos=ZPos, ActionType = 0, Name=groupName + SIGNALNAME + ACTIVNAME)
        # set_as_objectList(mission, smokeIDactivList, smokeIDList)
        # smokeIDdeActivList = copy_from_mission(mission, templateMission, Type=MCUCMDEFFECT, Name=TEMPLATECOMMAND)
        # set_kv(mission, smokeIDdeActivList, XPos=XPos, YPos=YPos, ZPos=ZPos, ActionType = 1, Name=groupName + SIGNALNAME + DEACTIVNAME)
        # set_as_objectList(mission, smokeIDdeActivList, smokeIDList)

        # ----------------------------------------
        # MCU to set trigger deactivating himself
        templateDeactivate = findObject(templateMission, Type=MCUDEACTIVATE, Name=TEMPLATEDEACTIVATE)
        deactivateNum = mission.MaxIndex + 1
        newDeactivate = templateMission.ObjList[templateDeactivate[0]].clone(deactivateNum)
        newDeactivate.setKv('Name', groupName + DEACTIVATENAME + str(compTriggerNum))
        XPos = XPos + PWCGsettings['DeltaX']
        newDeactivate.setKv(XPOS, XPos)
        ZPos = ZPos + PWCGsettings['DeltaZ']
        newDeactivate.setKv(ZPOS, ZPos)
        newDeactivate.PropList['Objects'] = {compTriggerNum}
        mission.addObject(newDeactivate, 0)

        #TODO add deactivate on takeoff event

    return compTriggerNum
