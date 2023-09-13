from basic_functions.find_object import findObject
from basic_functions.mission_class import Mission
from basic_functions.modify_object import get_kv, add_OnEvents
from basic_functions.properties_class import Properties
from declarations.properties_specials import XPOS, ZPOS, LINKTRID, \
    MCUCOUNTER, MCUTIMER, MCUDELETE, MCUBEHAVIOUR, AIRFIELD, MCUTR, STARTINAIR, EFFECT
from declarations.template_declaration import TEMPLATECOUNTER, TEMPLATETIMER, TEMPLATEDELETE, \
    TEMPLATEBEHAVIOUR, COUNTERNAME, TIMERNAME, DELETENAME, BEHAVIOURNAME, SETPLANESET, TEMPLATEAIRFIELD, TRNAME, \
    SETONSPAWN, TEMPLATESIGNALNAME, SIGNALNAME

lastX = -1
lastY = -1
lastZ = -1
# ---------------------------------------------
def createSpawnLogic(mission: Mission, planelist: list, groupName: str, airfieldList : list, PWCGsettings: dict, templateMission:Mission, escortInfoList:dict):
    """ create the logic for airfield activation for the selected flight """

    # SPAWN LOGIC => delete plane and set current planeset on each airfield
    # create counters for spawn
    for num in range(0,len(planelist)) :
        #create counter to delete plane and set according planeset
        planeNum =  planelist[num]
        createCounter(mission, num+1, planeNum, planelist, groupName, airfieldList, PWCGsettings,templateMission )

    # swpan activation for airfields (on report using linkID)
    # Build arfiled linIKD list
    linkIDSet = set()
    for airfieldNum in airfieldList:
        linkIDNo = mission.ObjList[airfieldNum].getKv(LINKTRID)
        linkIDSet.add(linkIDNo)

    #modifiy airfields LinkIDs to call counters
    #get counter of current group to call
    name = groupName+COUNTERNAME
    #counterList = findObject(mission, Type=MCUCOUNTER, Name=COUNTERNAME)
    counterList = findObject(mission, Type=MCUCOUNTER, Name=name)

    #build the on event list
    templateTR = findObject(templateMission, Type=MCUTR, Name=TRNAME)
    newProplist = list()
    # add counter to the property list in a loop
    for counter in counterList:
        newEventsProp = Properties('')
        newEventsProp.Value = dict()
        #get default format
        newEventsProp = templateMission.ObjList[templateTR[0]].PropList['OnEvents'][0].Value.copy()
        # modify
        newEventsProp['Type'] = SETONSPAWN
        newEventsProp['TarId'] = counter
        #add to the list
        prop = Properties(newEventsProp)
        newProplist.append(prop)

    #set the list for all linkID
    for linkIDNo in linkIDSet:
        mission.ObjList[linkIDNo].PropList['OnEvents'] = newProplist

# ---------------------------------------------
def createCounter(mission: Mission, num: int, planeNum: int, planelist: list, groupName: str, airfieldList : list, PWCGsettings: dict, templateMission:Mission):
    """ create counter to delete plane and set according planeset """

    counterList= list()

    #clone the counter
    templateCounter = findObject(templateMission, Type=MCUCOUNTER, Name = TEMPLATECOUNTER)
    coutnerNum = mission.MaxIndex + 1
    newCounter = templateMission.ObjList[templateCounter[0]].clone(coutnerNum)

    #clone the timer
    templateTimer = findObject(templateMission, Type=MCUTIMER, Name = TEMPLATETIMER)
    timerNum = coutnerNum + 1
    newTimer = templateMission.ObjList[templateTimer[0]].clone(timerNum)

    #clone the delete
    templateDelete = findObject(templateMission, Type=MCUDELETE, Name = TEMPLATEDELETE)
    deleteNum = timerNum + 1
    newDelete = templateMission.ObjList[templateDelete[0]].clone(deleteNum)

    #clone the change
    templateBehaviour = findObject(templateMission, Type=MCUBEHAVIOUR, Name = TEMPLATEBEHAVIOUR)
    behaviourNum = deleteNum + 1
    newBehaviour = templateMission.ObjList[templateBehaviour[0]].clone(behaviourNum)

    #set things
    # Counter
    newCounter.setKv('Name', groupName + COUNTERNAME + str(num))
    #set position
    if (mission.ObjList[planelist[len(planelist)-1]]).PropList[STARTINAIR] == 0 :
        #use plane
        XPos = mission.ObjList[planelist[len(planelist)-1]].getKv(XPOS) + PWCGsettings['DeltaX'] * (num - 1)
        ZPos = mission.ObjList[planelist[len(planelist)-1]].getKv(ZPOS) + PWCGsettings['DeltaZ']
    else:
        #use airfield
        XPos = mission.ObjList[airfieldList[0]].getKv(XPOS) + PWCGsettings['DeltaX'] * (num - 1)
        ZPos = mission.ObjList[airfieldList[0]].getKv(ZPOS) + PWCGsettings['DeltaZ']

    newCounter.setKv('XPos', XPos)
    newCounter.setKv('ZPos', ZPos)
    newCounter.setKv('Counter', num)
    # target the timer
    counterTargetSet = {timerNum}
    newCounter.PropList['Targets'] = counterTargetSet

    # Timer
    newTimer.setKv('Name', groupName+TIMERNAME+str(num))
    XPos = mission.ObjList[airfieldList[0]].getKv(XPOS)+PWCGsettings['DeltaX']*(num-1)
    newTimer.setKv('XPos', XPos )
    ZPos = mission.ObjList[airfieldList[0]].getKv(ZPOS) + PWCGsettings['DeltaZ']*2
    newTimer.setKv('ZPos', ZPos)
    newTimer.setKv('Time', PWCGsettings['DeactTimerDelay'])
    #target
    timerTargetSet = {deleteNum, behaviourNum}
    newTimer.PropList['Targets'] = timerTargetSet

    # Delete
    newDelete.setKv('Name', groupName+DELETENAME+str(planeNum))
    XPos = mission.ObjList[airfieldList[0]].getKv(XPOS)+PWCGsettings['DeltaX']*(num-1)
    newDelete.setKv('XPos', XPos )
    ZPos = mission.ObjList[airfieldList[0]].getKv(ZPOS) + PWCGsettings['DeltaZ']*3
    newDelete.setKv('ZPos', ZPos)
    # object
    #use planes in reverse order
    reverseList=sorted(planelist,reverse=True )
    planeLinkID = mission.ObjList[reverseList[num-1]].PropList[LINKTRID]
    deleteObjectSet = {planeLinkID}
    newDelete.PropList['Objects'] = deleteObjectSet

    # Behaviour
    # set planeset to -1 if last plane
    if num == len(planelist) :
        num=-1
    newBehaviour.setKv('Name', groupName+BEHAVIOURNAME+str(num))
    XPos = mission.ObjList[airfieldList[0]].getKv(XPOS)+PWCGsettings['DeltaX']*(num-1)+PWCGsettings['DeltaX']*0.5
    newBehaviour.setKv('XPos', XPos )
    ZPos = mission.ObjList[airfieldList[0]].getKv(ZPOS) + PWCGsettings['DeltaZ']*3
    newBehaviour.setKv('ZPos', ZPos)
    newBehaviour.setKv('FloatParam', num)
    newBehaviour.setKv('Filter', SETPLANESET)

    # object
    #find all airfields LinkID
    airfieldSet=set()

    for airfield in airfieldList:
        linkID = mission.ObjList[airfield].PropList[LINKTRID]
        airfieldSet.add(linkID)

    newBehaviour.PropList['Objects'] = airfieldSet


    #add objects
    mission.addObject(newCounter, 0)
    mission.addObject(newTimer, 0)
    mission.addObject(newDelete, 0)
    mission.addObject(newBehaviour, 0)

    counterList.append(coutnerNum)

    return counterList