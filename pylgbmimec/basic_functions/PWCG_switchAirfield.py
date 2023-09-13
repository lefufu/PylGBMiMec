import math

from basic_functions.find_object import findObject, findObjectInRange
from basic_functions.mission_class import Mission
from basic_functions.properties_class import Properties
from declarations.properties_specials import XPOS, ZPOS, LINKTRID, \
    MCUCOUNTER, MCUTIMER, MCUDELETE, MCUBEHAVIOUR, AIRFIELD, MCUTR, MCUWAYPOINT, MCUCTRIGGER, YPOS, COUNTRY, TIME, \
    ENABLED, MCUDEACTIVATE, MCUACTIVATE, EVENTENTER
from declarations.template_declaration import TEMPLATECOUNTER, TEMPLATETIMER, TEMPLATEDELETE, \
    TEMPLATEBEHAVIOUR, COUNTERNAME, TIMERNAME, DELETENAME, BEHAVIOURNAME, SETPLANESET, TEMPLATEAIRFIELD, TRNAME, \
    SETONSPAWN, BEHDEACTALL, SETCOUNTRY, TEMPLATECTRIGGER, CTRIGGERNAME, BEHAVAFNAME, AFTIMERNAME, TEMPLATEDEACTIVATE, \
    DEACTIVATENAME, TEMPLATEACTIVATE, ACTIVATENAME


# ---------------------------------------------
def createAirfieldSwich(mission: Mission, planelist: list, groupName: str, airfieldList : list, PWCGsettings: dict, templateMission:Mission):
    """ create the logic for switching airfield activated for spawn """

    # ------------------------------------------------
    #build airfield & linkID lists
    airfielLinkIDdSet = set()
    triggerList = list()

    #find  LinkID
    for airfield in airfieldList:
        linkID = mission.ObjList[airfield].PropList[LINKTRID]
        airfielLinkIDdSet.add(linkID)

    #------------------------------------------------
    # create a behaviour to deactivate all airfields
    templateBehaviour = findObject(templateMission, Type=MCUBEHAVIOUR)
    deactAllNum = mission.MaxIndex + 1
    newBehaviour = templateMission.ObjList[templateBehaviour[0]].clone(deactAllNum)
    newBehaviour.setKv('Name', groupName+BEHDEACTALL)

    XPos = mission.ObjList[airfieldList[0]].getKv(XPOS)+PWCGsettings['DeltaX']
    newBehaviour.setKv('XPos', XPos )
    ZPos = mission.ObjList[airfieldList[0]].getKv(ZPOS) + PWCGsettings['DeltaZ']*6
    newBehaviour.setKv('ZPos', ZPos)

    # set country to neutral
    newBehaviour.setKv('FloatParam', 0)
    newBehaviour.setKv('Filter', SETCOUNTRY)
    newBehaviour.PropList['Objects'] = airfielLinkIDdSet
    mission.addObject(newBehaviour, 0)

    #------------------------------------------------
    # process all airfields
    previousAirfield = -1
    num=0

    for airfield in sorted(airfielLinkIDdSet):
        #do nothing for 1st airfield = takeoff
        if previousAirfield != -1:
            posX = mission.ObjList[airfield].getKv(XPOS)
            posY = mission.ObjList[airfield].getKv(YPOS)
            posZ = mission.ObjList[airfield].getKv(ZPOS)
            prevPosX = mission.ObjList[previousAirfield].getKv(XPOS)
            prevPosY = mission.ObjList[previousAirfield].getKv(YPOS)
            prevPosZ = mission.ObjList[previousAirfield].getKv(ZPOS)
            distanceFromPrevious = math.sqrt((posX-prevPosX)*(posX-prevPosX) + (posZ-prevPosZ)*(posZ-prevPosZ))

            # ----------------------------------------
            #create new behaviour for current airfield
            templateBehaviour = findObject(templateMission, Type=MCUBEHAVIOUR)
            behaviourNum = mission.MaxIndex + 1
            newBehaviour = templateMission.ObjList[templateBehaviour[0]].clone(behaviourNum)
            newBehaviour.setKv('Name', groupName + BEHAVAFNAME+ str(num))

            XPos = posX
            newBehaviour.setKv(XPOS, XPos)
            ZPos = posZ + PWCGsettings['DeltaZ'] *3
            newBehaviour.setKv(ZPOS, ZPos)

            # set country to player country
            country = mission.ObjList[planelist[0]].getKv('Country')
            #newBehaviour.setKv('FloatParam', country )
            newBehaviour.setKv(COUNTRY, country)
            newBehaviour.setKv('Filter', SETCOUNTRY)
            #set object to current airfield
            newBehaviour.PropList['Objects'] = {airfield}
            mission.addObject(newBehaviour, 0)

            # ----------------------------------------
            #create timer for current airfield
            templateTimer = findObject(templateMission, Type=MCUTIMER)
            timerNum = mission.MaxIndex + 1
            newTimer = templateMission.ObjList[templateTimer[0]].clone(timerNum)
            newTimer.setKv('Name', groupName + AFTIMERNAME+ str(num))
            XPos = posX
            newTimer.setKv(XPOS, XPos)
            ZPos = posZ + PWCGsettings['DeltaZ'] * 2
            newTimer.setKv(ZPOS, ZPos)

            newTimer.setKv(TIME,  PWCGsettings['AFActivationDelay'])
            newTimer.PropList['Targets'] = {behaviourNum}


            #postponed to take into account deactivate MCU
            mission.addObject(newTimer, 0)

            # ----------------------------------------
            #create complex trigger
            templateCompTrigger = findObject(templateMission, Type=MCUCTRIGGER, Name=TEMPLATECTRIGGER)
            compTriggerNum = mission.MaxIndex + 1
            newcompTrigger = templateMission.ObjList[templateCompTrigger[0]].clone(compTriggerNum)
            newcompTrigger.setKv('Name', groupName + CTRIGGERNAME+str(num))
            newcompTrigger.setKv('Country', mission.ObjList[planelist[0]].getKv('Country'))
            #compute distance from previous airfield
            if distanceFromPrevious > PWCGsettings['MaxDetectionRadius']*2:
                distance = PWCGsettings['MaxDetectionRadius']
            else:
                distance = distanceFromPrevious/2
            newcompTrigger.setKv('Radius', distance)
            newcompTrigger.PropList['ObjectScript'] = [mission.ObjList[planelist[0]].getKv('Script')]

            newcompTrigger.setKv(XPOS, posX)
            newcompTrigger.setKv(YPOS, posY)
            newcompTrigger.setKv(ZPOS, posZ)

            #print((newcompTrigger.PropList['OnEvents'][0]) )

            newProplist = list()
            #for each event create a set
            # newcompTrigger.PropList['Targets'] = {timerNum, deactAllNum}
            for target in (timerNum, deactAllNum):
                newEventSetProp = Properties('')
                newEventSetProp.Value = dict()
                newEventSetProp = templateMission.ObjList[templateCompTrigger[0]].PropList['OnEvents'][0].Value.copy()
                newEventSetProp['Type'] = EVENTENTER
                newEventSetProp['TarId'] = target

                prop = Properties(newEventSetProp)
                newProplist.append(prop)

            # modify the airfield to use the list
            newcompTrigger.PropList['OnEvents'] = newProplist

            #if 1st waypoint, trigger is activated by default
            if num == 1 :
                newcompTrigger.setKv(ENABLED, 1)

            mission.addObject(newcompTrigger, 0)
            triggerList.append(compTriggerNum)

            # ----------------------------------------
            # MCU to set trigger deactivating himself
            templateDeactivate = findObject(templateMission, Type=MCUDEACTIVATE, Name=TEMPLATEDEACTIVATE)
            deactivateNum = mission.MaxIndex + 1
            newDeactivate = templateMission.ObjList[templateDeactivate[0]].clone(deactivateNum)
            newDeactivate.setKv('Name', groupName + DEACTIVATENAME+ str(num))
            XPos = posX + PWCGsettings['DeltaX'] * 2
            newDeactivate.setKv(XPOS, XPos)
            ZPos = posZ + PWCGsettings['DeltaZ'] * 3
            newDeactivate.setKv(ZPOS, ZPos)
            newDeactivate.PropList['Objects'] = {compTriggerNum}
            mission.addObject(newDeactivate, 0)

            #update trigger
            mission.ObjList[timerNum].PropList['Targets']= {behaviourNum, deactivateNum}

        previousAirfield = airfield
        num = num + 1

    #setup logic to chain triggers activation
    chainTriggers(mission, planelist, triggerList, groupName,  airfieldList, PWCGsettings, templateMission)

# ---------------------------------------------
def chainTriggers(mission: Mission,  planelist: list, triggerList:list, groupName: str, airfieldList : list, PWCGsettings: dict, templateMission:Mission):
    """ chain triggers to deactivate current one and activate the next one"""

    #browse all complex trigger of group
    for triggerRank in range(len(triggerList)):
        if triggerRank+1 < len(triggerList):
            trigger = triggerList[triggerRank]
            # get next trigger
            nextTrigger = triggerList[triggerRank+1]
            # ----------------------------------------
            # create a new activate MCU

            posX = mission.ObjList[trigger].getKv(XPOS)
            posY = mission.ObjList[trigger].getKv(YPOS)
            posZ = mission.ObjList[trigger].getKv(ZPOS)

            templateActivate = findObject(templateMission, Type=MCUACTIVATE, Name=TEMPLATEACTIVATE)
            activateNum = mission.MaxIndex + 1
            newActivate = templateMission.ObjList[templateActivate[0]].clone(activateNum)
            newActivate.setKv('Name', groupName + ACTIVATENAME+ str(nextTrigger ))
            XPos = posX + PWCGsettings['DeltaZ'] * 2.0
            newActivate.setKv(XPOS, XPos)
            ZPos = posZ + PWCGsettings['DeltaZ'] * 3.0
            newActivate.setKv(ZPOS, ZPos)
            newActivate.PropList['Objects'] = {nextTrigger}
            mission.addObject(newActivate, 0)

            #find timer associated to trigger => should be the max ID
            timerNum=0
            for event in range(len(mission.ObjList[trigger].PropList['OnEvents'])):
                objID = mission.ObjList[trigger].PropList['OnEvents'][event].Value['TarId']
                if objID > timerNum :
                    timerNum = objID
            newSet = set()
            for target in mission.ObjList[timerNum].PropList['Targets']:
                newSet.add(target)
            newSet.add(activateNum)
            mission.ObjList[timerNum].PropList['Targets'] = newSet
