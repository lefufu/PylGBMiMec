#  Contain function do add or remove objects in groups

# ---------------------------------------------
from basic_functions.mission_class import Mission

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