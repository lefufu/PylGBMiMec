#from typing import List, Any
from .file_functions import getBegining, readGroupFromFile, readObjectFromFile
from .object_class import *
from ..declarations.map_size import *
from ..declarations.properties_specials import GUIMAP, OPTIONS, GROUP, XPOS, ZPOS

class Mission:
    """Mission Class, contain an array of AllObject objects

    ObjList[] : AllObject
    dict of AllObject, contain all objects, including groups

    ObjIndex : dictionnary of dictionnary
    Index of object by type and area to speedup searching. Map is splitted into 16 zone
    eg : ObjIndex['Plane']['03'] = list of all plane object Index defined in 1st row fourth column of map

    MaxIndex : int
    maximum Index of all objects

    Xmin: float
    min X coordinate of the current map

    Xmax: float
    max X coordinate of the current map

    Zmin: float
    min Z coordinate of the current map

    Zmax: float
    max Z coordinate of the current map

    splitNB : int
    number of X/Z sector to use for indexing

    fileName : str
    name of input filename

    Methods
    -------
    addObject
    add a new object to mission
    """

    def __init__(self) -> object:
        """ create Mission
        """
        self.ObjList = dict()
        self.ObjIndex = dict()
        self.MaxIndex: int = 0
        self.Xmin: float = 0.0
        self.Xmax: float = 0.0
        self.Zmin: float = 0.0
        self.Zmax: float = 0.0
        self.splitNB: int = 0
        self.FileName: str = ''
# ---------------------------------------------
    def __str__(self):
        ''' convert mission in something that can be displayed'''
        convert2str=''
        convert2str += "Map : "+self.ObjList[0].PropList[GUIMAP]
        convert2str += "\nTotal number of objects : " + str(len(self.ObjList))
        for index in self.ObjIndex:
            convert2str+='\n   '+index+" : "+str(self.ObjIndex[index]['nb'])
        convert2str += '\n maximum Index number : '+str(self.MaxIndex)
        return convert2str

# ---------------------------------------------
    def addObject(self, Object:AllObject, level:int=0):
        """add an object to the mission object list"""

        if Object.type != OPTIONS:
            #TODO: implement group handling (not working)

            # Add object to object list
            objIndex = Object.getKv(INDEX)
            self.ObjList[objIndex] = Object

            if level != 0:
                Object.Level=level
            #add object to index list
            #intialize entry for object type
            if Object.type not in self.ObjIndex:
                self.ObjIndex[Object.type] = dict()
                for i in range(SPLIT_MAP):
                    for j in range(SPLIT_MAP):
                        self.ObjIndex[Object.type][str(i) + str(j)] = list()
                        self.ObjIndex[Object.type]['nb'] = 0

            if Object.type == GROUP :
                #some object like group does not have coordinate
                grid='00'
            else:
                # find grid
                grid=findGrid(self, Object)
            #initialize index
            if objIndex not in self.ObjIndex[Object.type][grid]:
                self.ObjIndex[Object.type][grid].append(objIndex)
                self.ObjIndex[Object.type]['nb']+=1

            #update global index
            if Object.getKv(INDEX) > self.MaxIndex:
                self.MaxIndex = objIndex
        else:
            # Mission option => intialize things
            #Option field => store object in 0 index
            self.ObjList[0] = Object
            #update map info
            mapName = Object.PropList[GUIMAP]
            mapFound=0
            for map in map_size:
                if map in mapName:
                    self.Xmin = map_size[map]['XMin']
                    self.Zmin = map_size[map]['ZMin']
                    self.Xmax = map_size[map]['XMax']
                    self.Zmax = map_size[map]['ZMax']
                    self.splitNB = SPLIT_MAP
                    mapFound = 1
            if not mapFound:
                criticalError(MAP_NOT_FOUND.format(mapName))

    # ---------------------------------------------
    def removeObjectFromIndex(self, objID:int):
        """remove an object from the index list of the mission
            :param typeObj: str
                type of object
            :param objID: int
                object ID to remove
        """

        typeObj=self.ObjList[objID].type
        for area in self.ObjIndex[typeObj]:
            if area != 'nb':
                if objID in self.ObjIndex[typeObj][area]:
                    self.ObjIndex[typeObj][area].remove(objID)
        return

    # ---------------------------------------------
    def removeObjectFromList(self, objID:int):
        """remove an object from the index list of the mission
            :param typeObj: str
                type of object
            :param objID: int
                object ID to remove
        """
        print(self.ObjList[objID])
        self.ObjList.pop(objID)
        return
    # ---------------------------------------------
    def setWindLayer(self, new_wind_layer_dictionary: dict):
        for i, altitude in enumerate([0, 500, 1000, 2000, 5000]):
            direction = new_wind_layer_dictionary[altitude]['direction']
            speed = new_wind_layer_dictionary[altitude]['speed']
            new_value = '    {0} :     {1} :     {2};\n'.format(altitude, direction, speed)
            self.ObjList[0].PropList['WindLayers'][i].Value = new_value
        return
#---------------------------------------------
def readMissionFromFile(mission:Mission, fileName: str) -> object:
        """ Read mission from IL2 GB .mission file"""
        filePointer=open(fileName)
        if not filePointer:
            criticalError(CAN_NOT_OPEN_FILE.format(fileName))
        mission.FileName=fileName
        #get first object type
        last_pos = filePointer.tell()
        objectType = getBegining(filePointer)
        filePointer.seek(last_pos)

        #must start by "Options"
        if objectType != OPTIONS:
            criticalError(MISSION_FILE_WITHOUT_OPTION)
        else:
            #read all objects
            endOfFile=0
            while not endOfFile:
                last_pos = filePointer.tell()
                objectType = getBegining(filePointer)
                filePointer.seek(last_pos)
                if objectType == GROUP:
                    readGroupFromFile(filePointer, 0, mission)
                elif objectType !='':
                    newObject=readObjectFromFile(filePointer)
                    mission.addObject(newObject)
                else:
                   endOfFile=1

        filePointer.close()

#---------------------------------------------
def findGrid(mission:Mission, object:AllObject):
    """ find Grid sector of an object (not linked to map numpad """
    XCoord = object.getKv(XPOS)
    ZCoord = object.getKv(ZPOS)
    Xgrid = int(XCoord / ((mission.Xmax - mission.Xmin) / mission.splitNB))
    Zgrid = int(ZCoord / ((mission.Zmax - mission.Zmin) / mission.splitNB))
    # fix for object placed outside the map
    if Xgrid < 0: Xgrid=0
    if Xgrid > (SPLIT_MAP-1) : Xgrid = SPLIT_MAP-1
    if Zgrid < 0: Zgrid=0
    if Zgrid > (SPLIT_MAP-1) : Zgrid = SPLIT_MAP-1
    grid = str(Xgrid) + str(Zgrid)
    return grid

#---------------------------------------------
def rangeGrid(mission, XRange=None, ZRange=None):
    """ return grid coordinate for Xrange or YRange """
    xmin=mission.Xmin
    xmax=mission.Xmax
    zmin=mission.Zmin
    zmax=mission.Zmax

    gridRetained=list()

    if XRange and type(XRange) is range :
        xmin = mission.Xmax
        xmax = mission.Xmin
        for i in XRange:
            if i < xmin:
                xmin = i
            if i > xmax:
                xmax = i
        i+=1
        if i > xmax:
             xmax = i

    if ZRange and type(ZRange) is range :
        zmin = mission.Zmax
        zmax = mission.Zmin
        for i in ZRange:
            if i < zmin:
                zmin = i
            if i > zmax:
                zmax = i
        i+=1
        if i > zmax:
             zmax = i

    xgridMin = int(xmin / ((mission.Xmax - mission.Xmin) / mission.splitNB))
    xgridMax = int(xmax / ((mission.Xmax - mission.Xmin) / mission.splitNB))
    zgridMin = int(zmin / ((mission.Zmax - mission.Zmin) / mission.splitNB))
    zgridMax = int(zmax / ((mission.Zmax - mission.Zmin) / mission.splitNB))

    for gridX in range(xgridMin, xgridMax+1):
        for gridZ in range(zgridMin, zgridMax+1):
            gridRetained.append(str(gridX)+str(gridZ))

    return gridRetained
