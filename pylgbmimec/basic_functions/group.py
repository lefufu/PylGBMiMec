#  Contain function do add or remove objects in groups

from basic_functions.mission_class import Mission

# ---------------------------------------------
def addInGroup(mission:Mission, groupID:int, objlist:list):
    """
    :param mission: Mission
        mission containing group to modify
    :param groupID: int
        ID of group in which to add objlist
    :param objList: list
        list of object ID to add in group

    """
    for objID in objlist:
        mission.ObjList[groupID].PropList['Objects'].add(objID)

# ---------------------------------------------
def addInGroup(mission:Mission, groupID:int, objID:int):
    """
    :param mission: Mission
        mission containing group to modify
    :param groupID: int
        ID of group in which to add objlist
    :param objID: list
        ID object to add in group

    """
    mission.ObjList[groupID].PropList['Objects'].add(objID)

# ---------------------------------------------
def findGroup(mission:Mission, objID:int):
    """ find group containing objID, if any
    :param mission: Mission
        mission containing group to modify
    :param objID: list
        ID object for which group is to be found

    """

    groupID=0
    for group in mission.ObjIndex['Group']['00']:
        if objID in mission.ObjList[group].PropList['Objects']:
            groupID=group

    return groupID

# ---------------------------------------------
def removeFromGroup(mission:Mission, groupID:int, objID:int):
    """
    remove objID from group groupID
    :param mission: Mission
        mission containing group to modify
    :param groupID: int
        ID of group in which to add objlist
    :param objID: list
        ID object to add in group

    """
    #remove object from group
    mission.ObjList[groupID].PropList['Objects'].remove(objID)

    return