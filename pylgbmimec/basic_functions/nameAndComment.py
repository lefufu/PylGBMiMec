from basic_functions.mission_class import Mission
from declarations.properties_specials import LCNAME, LCDESC

def createComment(mission: Mission, object, name: str, comment:str):
    """ Add an entry in the comment table """
    # create associated langage entries
    lastlabelNo = max(mission.LabelsList.keys())
    lastlabelNoName = lastlabelNo + 1
    lastlabelNoComment = lastlabelNo + 2
    mission.LabelsList[lastlabelNoName] = name
    mission.LabelsList[lastlabelNoComment] = comment

    if type(object) == int:
        (mission.ObjList[object]).PropList[LCNAME] = lastlabelNoName
        (mission.ObjList[object]).PropList[LCDESC] = lastlabelNoComment

    elif type(object) == list :
        print(mission.ObjList[object[0]])
        mission.ObjList[object[0]].PropList[LCNAME] = lastlabelNoName
        mission.ObjList[object[0]].PropList[LCDESC] = lastlabelNoComment

    else :
        object.setKv(LCNAME, lastlabelNoName)
        object.setKv(LCDESC, lastlabelNoComment)
