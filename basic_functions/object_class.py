from basic_handling.properties_class import *
from basic_handling.strProp import StrProp
from basic_handling.warning_handling import warning_msg, DUPLICATE_PROPERTIE
from declarations.properties_specials import LINKTRID, COMPLEXTRIGGERCOMMONPROP, OBJECTSCRIPT, TARGETS, OBJECTS, INDEX, \
    NAME, DUPLICATE_CTRIGGER


class AllObject:
    """ parent class for all object
    contain all common features
    type : str
    object type
    PropList : Properties{}
    dict of object properties
    level : int
    group level of object - 0 by default

    Methods
    -------
    addprop :
    add a new propertie and its value

    getKv :
    Get propertie value
    """
# ---------------------------------------------
    def __init__(self, type: str, level:int=0) -> object:
        """ create basic object with type and optional level parameter
        """
        self.type = type
        self.PropList = dict()
        self.Level = level

    def __init__(self, level:int=0) -> object:
        """ create basic object with no parameters
        """
        self.type = ''
        self.PropList = dict()
        self.Level = level
#---------------------------------------------
    def clear(self):
        """
        Clear object
        """
        self.type = ''
        self.PropList = dict()
        self.Level = 0
# ---------------------------------------------
    def AddProp(self, propertieName: str, propertieValue: object):
        """Add a propertie to object (used for create method) """
        if propertieName != OBJECTSCRIPT:
            if propertieName in self.PropList and propertieName not in DUPLICATE_CTRIGGER:
                warning_msg(DUPLICATE_PROPERTIE.format(propertieName, self.PropList[INDEX]))
            else:
                self.PropList[propertieName]=propertieValue
        else:
            # handle multiple "ObjectScript" lines for complex MCU => should be tupple ?
            if OBJECTSCRIPT not in self.PropList:
                self.PropList[OBJECTSCRIPT]=list()
            self.PropList[OBJECTSCRIPT].append(propertieValue)

# ---------------------------------------------
    def getKv(self, propertieName: str) -> object:
        """get key / value propertie"""
        if propertieName in self.PropList:
            return(self.PropList[propertieName])
        else:
            CriticalError(INVALID_PROP_NAME_FOR_GET.format(propertieName,self))
 # ---------------------------------------------
    def setKv(self, propertieName: str, value:object) -> object:
        """ set key Value propertie for an Object"""
        result=0
        if type(self.PropList[propertieName]) == str:
            self.PropList[propertieName] = "\""+str(value)+"\""
            result=1
        if type(self.PropList[propertieName]) == float:
            self.PropList[propertieName] = float(value)
            result=1
        if type(self.PropList[propertieName]) == int:
            self.PropList[propertieName] = int(value)
            result=1
        return(result)
# ---------------------------------------------
    def AddTarget(self, targetList):
        """ add one ID or a list of ID as targets
        """
        if TARGETS not in self.PropList:
            self.PropList[TARGETS]=set()
        if type(targetList) is list :
            for i in targetList:
                #self.PropList["Targets"]=self.PropList["Targets"].union(set(targetList))
                if i != self.PropList[INDEX]:
                    self.PropList[TARGETS].add(int(i))
        elif type(targetList) is int or type(targetList) is float:
            self.PropList[TARGETS].add(int(targetList))
        else :
            CriticalError(INVALID_TARGET_TYPE.format(targetList, self))

# ---------------------------------------------
    def SetTarget(self, targetList):
        """ set one ID or a list of ID as targets
        """
        self.PropList[TARGETS]=set()
        self.AddTarget(self, targetList)
 # ---------------------------------------------
    def AddObject(self, objectList):
        """ add one ID or a list of ID as objects
        """
        if OBJECTS not in self.PropList:
            self.PropList[OBJECTS]=set()
        if type(objectList) is list :
            for i in objectList:
                if i != self.PropList[INDEX]:
                    self.PropList[OBJECTS].add(int(i))
        elif type(objectList) is int or type(objectList) is float:
            self.PropList[OBJECTS].add(int(objectList))
        else:
            CriticalError(INVALID_OBJECT_TYPE.format(objectList, self))
# ---------------------------------------------
    def SetObject(self, objectList):
        """ set one ID or a list of ID as objects
        """
        self.PropList[OBJECTS]=set()
        self.AddObject(objectList)

# ---------------------------------------------
    def __str__(self):
        begin=offset(self)
        convert2str = begin+self.type + "\n"+begin+"{"
        for propName in self.PropList:
            convert2str +="\n"+begin+StrProp(propName, self.PropList[propName])
        convert2str +="\n"+ begin+ "}"
        return convert2str

# ---------------------------------------------
    def clone(self, newIndex:int):
        """clone current object into a new one,set new index"""
        newObject = AllObject()
        newObject.PropList=self.PropList.copy()
        newObject.setKv(INDEX,newIndex)
        oldName=self.getKv(NAME)
        newName=oldName.replace('\"', '')
        newObject.setKv(NAME,newName+"_cloned")
        return newObject

# ---------------------------------------------
    def cloneWithLinkedEntityProp(self, newIndex:int, mission):
        """clone current object into a new one, and include properties of linekdTR object.
        Not to be used except for creating temp obejct for find or scan functions"""
        newObject = AllObject()
        newObject.PropList=self.PropList.copy()
        newObject.setKv(INDEX,newIndex)
        #oldName=self.getKv(NAME)
        #newName=oldName.replace('\"', '')
        #newObject.setKv(NAME,newName+"_cloned")
        # have a look in linked entity if any, by recursive calling
        if LINKTRID in self.PropList:
            if self.PropList[LINKTRID] != 0:
                #add properies of linked object no beeing common
                for propname in mission.ObjList[self.PropList[LINKTRID]].PropList:
                    if propname not in COMPLEXTRIGGERCOMMONPROP:
                        newObject.PropList.update({propname:mission.ObjList[self.PropList[LINKTRID]].PropList[propname]})
        return newObject

# ---------------------------------------------
def offset(object:AllObject):
    """ find offset to add when printing"""
    begin = ''
    for i in range(0, object.Level):
        begin += "    "
    return begin
