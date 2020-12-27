#  Contain function do modify list of object
#  User level :
from .error_handling import *
from .find_object import findObject
from .group import findGroup, removeFromGroup
from .mission_class import Mission, Properties
from .warning_handling import warning_msg, PROP_TO_MODIFY_NOT_EXISTS, ENTITY_NOT_LINKED, \
    PROP_NOT_EXISTING, PROP_NOT_EXISTING_FOR_MOD
from ..declarations.envent_definitions import findEvent
from ..declarations.properties_specials import ONREPORTS, ONEVENTS, LINKTRID, NAME, INDEX, TYPE, CMDID, TARID, \
    OBJECTSCRIPT, COUNTRIES, COUNTRY, ONREPORT, ONEVENT
from ..declarations.report_definitions import findReport

# ---------------------------------------------
def modify_kv(mission:Mission, objList:list, **properties):
    """ modify key Value properties for a list of objects
        :param mission: Mission
           mission containing objects to modify
        :param objList: list
            list of object ID to modify
        :param properties : dict
            list of key / value to modify
    """
    #not really used...
    status=0

    for objIndex in objList:
        for key, val in properties.items():
            if key in mission.ObjList[objIndex].PropList:
                value=val
                if key == INDEX:
                    criticalError(CAN_NOT_MODIFY_INDEX.format(objIndex))

                if callable(val):
                    value=val(mission.ObjList[objIndex])
                if type(mission.ObjList[objIndex].PropList[key]) == float:
                    mission.ObjList[objIndex].PropList[key]=float(value)
                if type(mission.ObjList[objIndex].PropList[key]) == int:
                    mission.ObjList[objIndex].PropList[key]=int(value)
                if type(mission.ObjList[objIndex].PropList[key]) == str:
                    #check if " is in tring, otherwhise add it
                    strValue=str(value)
                    temp = strValue.find('\"')
                    if temp == -1:
                        strValue='\"'+strValue+'\"'
                    mission.ObjList[objIndex].PropList[key]=str(strValue)

            elif LINKTRID in mission.ObjList[objIndex].PropList:
                #test if prop exists in linked entity
                linkTRID = mission.ObjList[objIndex].PropList[LINKTRID]
                tempdict={key:val}
                if  linkTRID != 0:
                    # try to update prop in object
                    tempList=[linkTRID]
                    status=modify_kv(mission,tempList , **tempdict)
            else:
                # prop not existing for object
                name=""
                if NAME in mission.ObjList[objIndex].PropList:
                    name=mission.ObjList[objIndex].PropList[NAME]
                warning_msg(PROP_TO_MODIFY_NOT_EXISTS.format(key,objIndex,name))

    return status

# ---------------------------------------------
def add_in_targetList(mission:Mission, objList:list, targetList:list):
    """ add target(s) to object target list
    :param mission: Mission
            mission containing objects to modify
    :param objList: list
            list of object ID to modify
    :param targetList: list
            list of object ID to add at target list
    """
    #unused
    status=0

    for objID in objList:
        mission.ObjList[objID].addTarget(targetList)
    return status

# ---------------------------------------------
def set_as_targetList(mission: Mission, objList: list, targetList: list):
    """ set target(s) to object target  list
    :param mission: Mission
            mission containing objects to modify
    :param objList: list
            list of object ID to modify
    :param targetList: list
            list of object ID to set as target list
    """
    # unused
    status = 0

    for objID in objList:
        mission.ObjList[objID].setTarget(targetList)

    return status


# ---------------------------------------------
def add_in_objectList(mission: Mission, objList: list, targetList: list):
    """ add target(s) to object object list
    :param mission: Mission
            mission containing objects to modify
    :param objList: list
            list of object ID to modify
    :param targetList: list
            list of object ID to add at Object list
    """
    # unused
    status = 0

    for objID in objList:
        mission.ObjList[objID].addObject(targetList)
    return status


# ---------------------------------------------
def set_as_objectList(mission: Mission, objList: list, targetList: list):
    """ set target(s) to object object list
    :param mission: Mission
            mission containing objects to modify
    :param objList: list
            list of object ID to modify
    :param targetList: list
            list of object ID to set as Object list
    """
    # unused
    status = 0

    for objID in objList:
        mission.ObjList[objID].SetObject(targetList)

    return status
# ---------------------------------------------
def add_OnReports(mission: Mission, objList: list, reportName:str, commandID:list, targetID: list, reset=0):
    """ add targetList objects for event reportNumber of objects objList
    :param mission: Mission
            mission containing objects to modify
    :param objList: list
            list of object ID to modify
    :param reportName: str
            name of report (see declarations\report_definition.py)
    :param commandID: list
            object ID to use as command, in a list comming from "find object'
    :param targetID: list
            object ID to use as target, in a list comming from "find object'
    :param reset: int
            if set to 1 reset Report list
"""
    for obj in objList:
        #Find MCU_TR_Entity associated to object
        if LINKTRID in mission.ObjList[obj].PropList:
            linkTrId=mission.ObjList[obj].PropList[LINKTRID]
            if linkTrId == 0:
                warning_msg(ENTITY_NOT_LINKED.format(obj,'add_OnReport'))
            else:
                if reset == 1 or ONREPORTS not in mission.ObjList[linkTrId].PropList:
                    # reset or create OnReports list
                    mission.ObjList[linkTrId].PropList[ONREPORTS]=list()
                #create a new propertie and add it to the 'OnReports' list
                prop = Properties('')
                prop.Value = dict()
                prop.Value[TYPE] = findReport(mission.ObjList[obj].type, reportName)
                prop.Value[CMDID] = commandID[0]
                prop.Value[TARID] = targetID[0]
                prop.Value['LIST_NAME;'] = ONREPORT
                mission.ObjList[linkTrId].PropList[ONREPORTS].append(prop)
        else:
            warning_msg(ENTITY_NOT_LINKED.format(obj, 'add_OnReport'))

# ---------------------------------------------
def set_OnReports(mission: Mission, objList: list, reportName:str, commandID:list, targetID: list):
    """ add targetList objects for event reportNumber of objects objList
    :param mission: Mission
            mission containing objects to modify
    :param objList: list
            list of object ID to modify
    :param reportName: str
            name of report (see declarations\report_definition.py)
    :param commandID: list
            object ID to use as command, in a list comming from "find object'
    :param targetID: list
            object ID to use as target, in a list comming from "find object'
"""
    add_OnReports(mission, objList, reportName, commandID, targetID, reset=1)

# ---------------------------------------------
def add_OnEvents(mission: Mission, objList: list, eventName:str, targetID: list, reset=0):
    """ add targetList objects for event reportNumber of objects objList
    :param mission: Mission
            mission containing objects to modify
    :param objList: list
            list of object ID to modify
    :param reportName: str
            name of report (see declarations\report_definition.py)
    :param commandID: list
            object ID to use as command, in a list comming from "find object'
    :param targetID: list
            object ID to use as target, in a list comming from "find object'
    :param reset: int
            if set to 1 reset event list
"""
    for obj in objList:
        #Find MCU_TR_Entity associated to object
        if 'LinkTrId' in mission.ObjList[obj].PropList:
            linkTrId=mission.ObjList[obj].PropList[LINKTRID]
            if linkTrId == 0:
                warning_msg(ENTITY_NOT_LINKED.format(obj,'add_OnEvents'))
            else:
                if reset == 1 or ONEVENTS not in mission.ObjList[linkTrId].PropList:
                    # reset or create OnReports list
                    mission.ObjList[linkTrId].PropList[ONEVENTS]=list()
                #create a new propertie and add it to the 'OnReports' list
                prop = Properties('')
                prop.Value = dict()
                prop.Value[TYPE] = findEvent(mission.ObjList[obj].type, eventName)
                prop.Value[TARID] = targetID[0]
                prop.Value['LIST_NAME;'] = ONEVENT
                mission.ObjList[linkTrId].PropList[ONEVENTS].append(prop)
        else:
            warning_msg(ENTITY_NOT_LINKED.format(obj, 'add_OnEvents'))

# ---------------------------------------------
def set_OnEvents(mission: Mission, objList: list, reportName:str, targetID: list):
    """ add targetList objects for event reportNumber of objects objList
    :param mission: Mission
            mission containing objects to modify
    :param objList: list
            list of object ID to modify
    :param reportName: str
            name of report (see declarations\report_definition.py)
    :param commandID: list
            object ID to use as command, in a list comming from "find object'
    :param targetID: list
            object ID to use as target, in a list comming from "find object'
"""
    add_OnEvents(mission, objList, reportName, targetID, reset=1)

# ---------------------------------------------
def add_ObjScriptList(mission: Mission, objList: list, ObjScriptList:list=None, Countries:list=None, reset=0):
    """ add object scripts if provided and countries if provided in field "ObjectScript" and "country" of objects objList
    :param mission: Mission
            mission containing objects to modify
    :param objList: list
            list of object ID to modify : must be complex trigger
    :param objScriptList: list
            list of script names to add (can be empty if only countries are to be added)
    :param countries: list
           list of countries ID to add (can be empty if only script names are to be added)
    :param reset: int
           optional if set to 1 reset script and country list
"""
    # for all objects try to update prop
    for obj in objList:
        #check if prop OBJECTSCRIPT exists
        if OBJECTSCRIPT not in mission.ObjList[obj].PropList:
            warning_msg(PROP_NOT_EXISTING_FOR_MOD.format(OBJECTSCRIPT,obj))
        else:
            # update the prop obj script if param not empty
            if ObjScriptList:
                if reset == 1:
                    mission.ObjList[obj].PropList[OBJECTSCRIPT] = list()
                for scriptName in ObjScriptList:
                    # fix in case of " missing
                    if '\"' not in scriptName:
                        scriptName='\"'+scriptName+'\"'
                    mission.ObjList[obj].PropList[OBJECTSCRIPT].append(scriptName)

        # check if prop COUNTRIES exists
        if COUNTRY not in mission.ObjList[obj].PropList:
            warning_msg(PROP_NOT_EXISTING_FOR_MOD.format(COUNTRY,obj))
        else:
            # update the prop obj script if param not empty
            if Countries:
                if reset == 1:
                    mission.ObjList[obj].PropList[COUNTRY] = list()
                for countryID in Countries:
                    mission.ObjList[obj].PropList[COUNTRY].append(countryID)
    return

# ---------------------------------------------
def set_ObjScriptList(mission: Mission, objList: list, ObjScriptList:list=None, Countries:list=None):
    """ replace current object scripts list if provided and current countries if provided by new ones for objects in objList
    :param mission: Mission
            mission containing objects to modify
    :param objList: list
            list of object ID to modify : must be complex trigger
    :param objScriptList: list
            list of script names to add (can be empty if only countries are to be added)
    :param countries: list
           list of countries ID to add (can be empty if only script names are to be added)

"""
    add_ObjScriptList(mission, objList, ObjScriptList, Countries, reset = 1)

#---------------------------------------------
#TODO : delete object
def deleteObject(mission:Mission, objList:list):
    """ delete a list of object in the mission
        :param mission: Mission
            mission containing objects to delete
        :param objList: list
            list of object ID to modify
    """

    for objID in objList:
        # remove object in groups
        groupID = findGroup(mission,objID)
        if groupID:
            removeFromGroup(mission,groupID,objID)

        linkTrID=mission.ObjList[objID].getKv(LINKTRID)

        # if object is linktrID-ed it can be referecend by other objects
        if linkTrID:
            # remove in objects fields of other objects
            inObjectList=findObject(mission, Objects=objID)
            for objID2 in inObjectList:
                obList=mission.ObjList[objID2].PropList['Objects']
                #field to remove is the LINKTRID and not the object id !
                obList.discard(linkTrID)
                mission.ObjList[objID2].SetObject(obList)

            # remove in target fields of other objects
            inTargetList=findObject(mission, Targets=objID)
            for objID2 in inTargetList:
                 objectList=mission.ObjList[objID2].PropList['Targets']
                 #field to remove is the LINKTRID and not the object id !
                 objectList.discard(linkTrID)
                 mission.ObjList[objID2].setTarget(objectList)

        # remove object in objIndex
        mission.removeObjectFromIndex(objID)

        # remove linktrID
        if linkTrID:
            deleteObject(mission,[linkTrID])

        # remove object in mission ObjList
        mission.removeObjectFromList(objID)

    return