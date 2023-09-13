#  Contain function do search object
#  User level : findObject, findObjectInRange

import math
import re
from basic_functions.mission_class import Mission, INVALID_TYPE_FOR_RANGE, criticalError, BAD_FILTER_RANGE, rangeGrid, \
    DOUBLE_RANGE_FILTER
from basic_functions.warning_handling import PROP_NOT_EXISTING, ONLY_FIRST_OBJECT_USED, warning_msg, EMPTY_CENTER, \
    TYPE_NOT_SUPPORTED_FOR_REQUEST

from declarations.properties_specials import XPOS, ZPOS, TYPE, GROUP, INDEX, NAME, OBJECTSCRIPT, OBJECTS, \
    EXCEPTION_FOR_FILTER, LINKTRID, TARGETS


# ---------------------------------------------
def findObject(mission:Mission, **parameters ):
    """find objects of a mission by using multiple criterion on parameters
            :param mission: Mission
            mission containing objects to search
            :param parameters: dict
            all criterion to search objects, separated by ,
            eg groupList = findObject(newMission, Type='Vehicle', Index=range(11,16), XPos=range(29000,29700), ZPos=range(25000,27000))
            filter criterions
            key=value
                eg: Name='Blue', Xpos=3.23, Type="Plane"
                if string is used fpr any key except Type, it will be used as regex. Eg 'Plane' = ok for every string containing 'Plane',
                    '^Plane$' ok only for string containing strictly Plane
                Type field must be the exact string with exact case
            key=range(min, max)
                eg Index=range(11,16), XPos=range(29000,29700)
                range value must be int but propertie can be float. Criterion will be ok if Range min <= key value <= Range Max
            :return list:
            list of object ID that fullfill criterions
     """
    listOfObject = list()
    dictOfFilter=dict()
    gridList = list()

    for key, val in parameters.items():
        if key != 'Type' and key != 'Group':
            dictOfFilter[key]=val

    #define Grid Range if Xpos or YPos are used
    XRange=range(0,0)
    YRange=range(0,0)
    if XPOS in parameters and ZPOS not in parameters:
        gridList = rangeGrid(mission, XRange=parameters[XPOS])
    elif  XPOS not in parameters and ZPOS in parameters:
        gridList = rangeGrid(mission, ZRange=parameters[ZPOS])
    elif XPOS in parameters and ZPOS in parameters:
        gridList = rangeGrid(mission, XRange=parameters[XPOS], ZRange=parameters[ZPOS])

    if 'FromPoint' in parameters:
        xRange=range(parameters['FromPoint'][0]-int(parameters['FromPoint'][2]/2), parameters['FromPoint'][0]+int(parameters['FromPoint'][2]/2))
        ZRange = range(parameters['FromPoint'][1]-int(parameters['FromPoint'][2]/2), parameters['FromPoint'][1]+int(parameters['FromPoint'][2]/2))
        gridList = rangeGrid(mission, XRange=xRange, ZRange=ZRange)

    #initiate list of object, either by type or Group
    # use pre filtering by type
    if TYPE in parameters:
        typeList=list()
        for typeObj in mission.ObjIndex:
            if re.search(parameters[TYPE], typeObj):
                if typeObj != GROUP :
                    typeList.append(typeObj)

        for typeObj in typeList:
            if len(gridList) == 0 :
                for tempgrid in mission.ObjIndex[typeObj]:
                    if tempgrid != 'nb':
                        gridList.append(tempgrid)
            for tmpGrid in gridList:
                if tmpGrid in mission.ObjIndex[typeObj]:
                    for index in mission.ObjIndex[typeObj][tmpGrid]:
                        listOfObject.append(index)

    if GROUP in parameters:
        # get Id of group object (recurivelly) and cross reference wiht type if defined
        listInGroup=getIndexInGroup(mission, parameters[GROUP])
        crossList=list()
        # if previous list of type has been find, then cross checked
        if len(listOfObject) != 0 :
            # cross reference
            for objIndex in listOfObject:
                if objIndex in listInGroup:
                    crossList.append(objIndex)
            listOfObject=crossList
        else:
            listOfObject=listInGroup

    #add  all objects except groups
    if not TYPE in parameters and not GROUP in parameters:
        for typeObject in mission.ObjIndex:
            if typeObject != GROUP:
                for grid in mission.ObjIndex[typeObject]:
                    if grid != 'nb':
                        for objIndex in mission.ObjIndex[typeObject][grid]:
                            listOfObject.append(objIndex)

    listOfObject = filterListOfObject(mission, listOfObject, dictOfFilter)

    # add  the object if not in list
    if 'Index' in parameters:
        listOfObject.append(parameters['Index'])

    return listOfObject
# ---------------------------------------------
def findObjectInRange(mission:Mission, centerObj:list, Range:int, **parameters):
    """find objects of a mission by using range from a given object and same filtering parameter as for findObject
            :param mission: Mission
            mission containing objects to search
            :param centerObj: list
            ID of object center of the range to search
            :param: range : int
            Radius of the circle around centerObj that whill be used to filter objects
            :param parameters: dict
            all criterion to search objects, separated by ,
            eg groupList = findObject(newMission, Type='Vehicle', Index=range(11,16), XPos=range(29000,29700), ZPos=range(25000,27000))
            filter criterions
            key=value
                eg: Name='Blue', Xpos=3.23, Type="Plane"
                if string is used fpr any key except Type, it will be used as regex. Eg 'Plane' = ok for every string containing 'Plane',
                    '^Plane$' ok only for string containing strictly Plane
                Type field must be the exact string with exact case
            key=range(min, max)
                eg Index=range(11,16), XPos=range(29000,29700)
                range value must be int but propertie can be float. Criterion will be ok if Range min <= key value <= Range Max
            :return list:
            list of object ID that fullfill criterions
     """
    filteredList = list()

    if 'FromPoint' in parameters:
        criticalError(DOUBLE_RANGE_FILTER)
    else:
        #if len(centerObj) == 0:
        #    warning_msg(EMPTY_CENTER)
        #elif len(centerObj) > 1:
        if type(centerObj) == list:
            warning_msg(ONLY_FIRST_OBJECT_USED.format(centerObj))
            center = centerObj[0]
        else:
            center = centerObj
        #create FromPoint parameter
        fromPointlist=list()
        fromPointlist.append(int(mission.ObjList[center].PropList[XPOS]))
        fromPointlist.append(int(mission.ObjList[center].PropList[ZPOS]))
        fromPointlist.append(Range)
        parameters['FromPoint']=fromPointlist
        filteredList = findObject(mission, **parameters)
    return filteredList

# ---------------------------------------------
def filterListOfObject(mission:Mission, objIndexList:list, dictOfFilter:dict ):
    """find objects of a mission by using and key = value parameters"""
    filteredList=list()
    for index in objIndexList:
        criterion = 0
        # create an object by cloning current object and its linked entity if any
        currentObj = mission.ObjList[index].cloneWithLinkedEntityProp(0, mission)

        for key, val in dictOfFilter.items():
            if key not in currentObj.PropList and key not in EXCEPTION_FOR_FILTER:
                warning_msg(PROP_NOT_EXISTING.format(key,mission.ObjList[index].PropList[INDEX]))
            elif key not in EXCEPTION_FOR_FILTER:
                #handle standard properties processing
                currentProp = currentObj.PropList[key]
                if  isinstance(val, str):
                    #handle string criterion
                    if re.search(val, str(currentProp).replace("\"","")):
                        criterion += 1
                elif isinstance(val, range):
                    #handle range criterion
                    rangeprobe=list(val)
                    if len(rangeprobe) == 0:
                        criticalError(BAD_FILTER_RANGE.format(val))
                    if isinstance(rangeprobe[0], int) and isinstance(currentProp, int):
                        # do iteration on range
                        fixedRange = list(range(rangeprobe[0], rangeprobe[len(rangeprobe)-1] + 2))
                        if index in fixedRange:
                            criterion += 1
                    elif isinstance(rangeprobe[0], int) and type(currentProp) == float:
                        #float values:  use min and max
                        if currentProp >= rangeprobe[0] and currentProp <= rangeprobe[len(rangeprobe)-1]:
                            criterion += 1
                    else :
                        criticalError(INVALID_TYPE_FOR_RANGE.format(type(currentObj.PropList[key]), key, val, currentObj.PropList[NAME]))
                else:
                    #handle direct comparison or list scanning
                    #unitary value
                    if type(currentObj.PropList[key]) == float or type(currentObj.PropList[key]) == int or type(currentObj.PropList[key]) == str:
                        #if mission.ObjList[index].PropList[key] == val:
                        if currentObj.PropList[key] == val:
                            criterion += 1
                    #TODO handle set (should be target, object)
                    elif type(currentObj.PropList[key]) == set:
                        if type(val) != int:
                            warning_msg(TYPE_NOT_SUPPORTED_FOR_REQUEST.format(type(val), key))
                        # object or Target are note referenced by their ID, but by their LINKTRID
                        if (key == OBJECTS or key == TARGETS) and LINKTRID in mission.ObjList[val].PropList:
                            val = mission.ObjList[val].PropList[LINKTRID]
                        if val in currentObj.PropList[key]:
                            criterion += 1
                    #TODO handle tupple : should be only 'ObjectScript'
                    elif type(currentObj.PropList[key]) == tuple:
                        if type(val) != str and key == OBJECTSCRIPT:
                            warning_msg(TYPE_NOT_SUPPORTED_FOR_REQUEST.format(type(val), key))
                        if val in currentObj.PropList[key]:
                            criterion += 1
            else:
                #FromProint
                Xcenter =val[0]
                Zcenter=val[1]
                radius=val[2]
                distanceX = (Xcenter-currentObj.PropList[XPOS])*(Xcenter-currentObj.PropList[XPOS])
                distanceZ = (Zcenter-currentObj.PropList[ZPOS])*(Zcenter-currentObj.PropList[ZPOS])
                distance = math.sqrt( distanceX+distanceZ )
                if (distance <= radius):
                    criterion+=1
        if criterion == len(dictOfFilter):
            filteredList.append(index)

    return filteredList

# ---------------------------------------------
def getIndexInGroup(mission, groupName):
    """ recursivelly scan group to return object list"""
    objectInGroup = list()
    for obj in mission.ObjIndex[GROUP]['00']:
        if mission.ObjList[obj].type == GROUP :
            #if re.search(groupName, mission.ObjList[obj].PropList[NAME].replace("\"","")):
            tempoName = "\"" +mission.ObjList[obj].PropList[NAME].replace("\"","") + "\""
            if re.search(groupName, tempoName) :
                for index in mission.ObjList[obj].PropList[OBJECTS]:
                    if mission.ObjList[index].type == GROUP:
                        subGroupName=mission.ObjList[index].PropList[NAME].replace("\"","")
                        subGrouplist=getIndexInGroup(mission, subGroupName)
                        objectInGroup+=subGrouplist
                    else:
                        objectInGroup.append(index)

    return objectInGroup

# ---------------------------------------------
def printObjects(mission:Mission, objectList:list):
    """ print a list of object """
    for objIndex in objectList:
        print(mission.ObjList[objIndex])

    return

# ---------------------------------------------
def findGroupByName(mission:Mission, GroupName:str):
    """find group of a mission by using name
           :param mission: Mission
           mission containing objects to search
           :param GroupName: str
           name of group to find
            :return list:
            list of group ID that fullfill criterions (should be one)
    """
    resultlist = list()

    for idGroup in mission.ObjIndex['Group']['00']:
        temp=mission.ObjList[idGroup].PropList['Name'].replace('\"','')
        if temp == GroupName:
            resultlist.append(idGroup)

    return resultlist