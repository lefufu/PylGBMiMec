#  Contain function do create object
#  User level :

from basic_functions.find_object import findObject, findGroupByName
from basic_functions.group import addInGroup
from basic_functions.mission_class import Mission

from basic_functions.object_class import AllObject
from declarations.properties_specials import INDEX, LINKTRID, MISOBJID, TARGETS


# ---------------------------------------------
def copy_from_mission(destMission:Mission, sourceMission:Mission, groupName=str, **parameter):
    """ copy all object of sourceMission that fullfill properties into destMission
        :param destMission: Mission
           mission containing the obejct to copy
        :param sourceMission:Mission
           mission that contain all object that can be copyed
        :param properties : dict
            list of key / value to select objets
    """
    # process group if needed
    level=0

    #find offset which will be added to new objects
    offset = destMission.MaxIndex+1

    addedObjects=list()

    if groupName:
        objlist=findGroupByName(destMission, groupName)
    if len(objlist) > 0:
        groupID = objlist[0]
        level=destMission.ObjList[groupID].Level
    else:
        groupID = 0

    # find objects and add them to target mission
    objList = findObject(sourceMission, **parameter )
    for objID in objList:
        sourceObj=sourceMission.ObjList[objID]
        newObject=AllObject()
        newObject.type = sourceObj.type
        newObject.PropList=sourceObj.PropList.copy()
        #newindex=destMission.MaxIndex+1
        newindex=sourceObj.getKv(INDEX) + offset
        newObject.setKv(INDEX,newindex)
        addedObjects.append(newindex)
        #not possible to add directly an object in mission in the group (group not existing in destmission when called with addObject...
        destMission.addObject(newObject,level)
        # Add object in group
        if groupID:
            addInGroup(destMission, groupID, newindex)

        #update  TARGET list
        oldtargetList=sourceObj.getTarget()
        if len(oldtargetList):
            #apply offset
            newTargetList=list()
            for target in oldtargetList:
                newTargetList.append(target+offset)
            newObject.setTarget(newTargetList)

        #update  OBJECT list
        oldObjectList=sourceObj.getObject()
        if len(oldObjectList):
            #apply offset
            newObjectList=list()
            for object in oldObjectList:
                newObjectList.append(object+offset)
            newObject.setObject(newObjectList)

        #update Linked entities
        if LINKTRID in sourceObj.PropList:
            oldLink=sourceObj.getKv(LINKTRID)
            if oldLink > 0:
                # create copy of LINKTRID
                #newlink=sourceObj.getKv(LINKTRID)+offset
                newlink=copy_from_mission(destMission, sourceMission, Index=oldLink)
                newObject.setKv(LINKTRID,newlink[0])
                (destMission.ObjList[newlink[0]]).setKv(MISOBJID, newindex)
                (destMission.ObjList[newlink[0]]).PropList[TARGETS]=set()

        if MISOBJID in sourceObj.PropList:
            oldLink=sourceObj.getKv(MISOBJID)
            if oldLink > 0:
                newlink=sourceObj.getKv(MISOBJID)+offset
                newObject.setKv(MISOBJID,newlink)

    return addedObjects