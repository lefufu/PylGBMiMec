""" package containing functions dedicated to file handling, including object formating"""
import re

from basic_functions.error_handling import *
from basic_functions.object_class import AllObject
from basic_functions.properties_class import Properties

#####################################################################################
from declarations.properties_specials import WINDLAYERS, COUNTRIES, CARRIAGES, LIST_OF_STRINGS, GROUP, INDEX, BOUNDARY
from declarations.template_declaration import GROUPOFFSET


def readPropFromFile(filePointer):
    """ read properties from file"""
    key = ""
    prop=Properties('')
    line = readLine(filePointer)
    if line == "":
        criticalError("unable to read object from file:" + str(filePointer))
    else:
        # find the kind of properties
        # test if unitary (key = value)
        keyValue = re.search(r"^\s*(?P<name>[^= ]*)\s*=\s*(?P<value>[^=]*)\s*;", line)
        endOfObject = re.search(r"^\s*}\s*$", line)
        nameOnly = re.search(r"^\s*(?P<name>[a-zA-Z0-9_]*)\s*[^;]$", line)
        isWindLayer =re.search(r"^\s*[0-9.]*\s*:\s*[0-9.]*\s*:\s*[0-9.]*\s*;$", line)
        isCountries = re.search(r"^\s*[0-9.]*\s*:\s*[0-9.]*\s*;$", line)
        #isCarriage = re.search(r"^\s*\"LuaScripts\\WorldObjects\\[Tt]rains\\\w*.\w*\"\s*;$", line)
        isCarriage = re.search(r"^\s*\"LuaScripts\\WorldObjects\\[Tt]rains\\[a-zA-Z0-9_-]*.\w*\"\s*;$", line)
        isBoundary = re.search(r"^\s*[0-9.]*\s*,\s*[0-9.]*\s*;$", line)

        if isWindLayer or isCountries or isCarriage or isBoundary:
            if isWindLayer:
                key = WINDLAYERS
            elif isCountries:
                key = COUNTRIES
            elif isCarriage:
                key = CARRIAGES
            else:
                key = BOUNDARY
            prop.Value = line

        elif keyValue:
            # Key / value
            key = keyValue.group('name')
            value = keyValue.group('value')
            # string value
            isString = re.search(r"^\s*\"\s*", value)
            isTime = re.search(r"^\s*[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}$", value)
            #isDate = re.search(r"^\s*[0-9]{1,2}.\.[0-9]{1,2}\.[0-9]{4}$", value)
            isDate = re.search(r"^\s*[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4}$", value)
            isArray = re.search(r"^\[[0-9,.\"\w\s]*\]$", value)

            if isString or isTime or isDate:
                # process value date or time
                prop.Value = str(value)

            elif isArray:
                # process array values, must be put in python set
                prop.Value = set()
                stringList = value.strip('][').split(",")
                for i in stringList:
                    isInt = re.search(r"^\s*[-+]?\d+\s*$", i)
                    isFloat = re.search(r"^\s*[+-]?([0-9]*[.])?[0-9]+$", value)
                    if isInt:
                        prop.Value.add(int(i))
                    elif isFloat:
                        prop.Value.add(float(i))
                    elif i != '':
                        prop.Value.add(i)
            else:
                # process string or numerical values
                isInt = re.search(r"^\s*[-+]?\d+\s*$", value)
                isFloat = re.search(r"^\s*[+-]?([0-9]*[.])?[0-9]+$", value)
                if isInt:
                    prop.Value = int(value)
                elif isFloat:
                    prop.Value = float(value)
                else:
                    criticalError(CAN_NOT_READ_PROPERTIE + "\"" + line + "\"")

        elif endOfObject:
            # End Of object: set value to "}" (already the case)
            value = "}"
        elif nameOnly:
            key = nameOnly.group('name')
            # check that next line is '{'
            line2 = readLine(filePointer)
            listOrDic = re.search(r"^\s*{\s*$", line2)
            if listOrDic:
                isDict = 0
                endOfList = 0
                # process properties in list. If first line is a key => value create dictionary
                last_pos = filePointer.tell()
                probeLine = readLine(filePointer)
                filePointer.seek(last_pos)
                probeKeyValue = re.search(r"^\s*(?P<name>[^= ]*)\s*=\s*(?P<value>[^=]*)\s*;", probeLine)
                if probeKeyValue:
                    prop.Value = dict()
                    isDict = 1
                else:
                    prop.Value = list()
                while endOfList == 0:
                    tempName, tempProp = readPropFromFile(filePointer)
                    if tempName != "":
                         if isDict:
                             prop.Value[tempName]=tempProp.Value
                         else:
                             #if tempName != 'WindLayers' and tempName != 'Countries' and tempName != 'Carriages':
                             if tempName not in LIST_OF_STRINGS:
                                 tempProp.Value["LIST_NAME;"]=tempName
                             prop.Value.append(tempProp)
                    else:
                        endOfList=1
            else:
                msg=CAN_NOT_READ_LIST_PROPERTIE.format(line)
                criticalError(msg)
        else:
            criticalError(CAN_NOT_READ_PROPERTIE + line)
    return key, prop

#####################################################################################
def readObjectFromFile(filePointer):
    """Read object from opened file """
    objectType = getBegining(filePointer)
    if objectType == '':
        criticalError(UNABLE_TO_FIND_OBJECT_BEGINING + str(filePointer))
    else:
        newObject=AllObject()

        EndOfObject = 0
        newObject.PropList = dict()
        newObject.type = objectType
        line = readLine(filePointer)
        # check if next line is "{"
        m = re.search(r"\s*{\s*$", line)
        if not m:
            criticalError(UNABLE_TO_READ_OBJECT_FROM_FILE + objectType + " from file:" + str(filePointer))
        else:
            while EndOfObject == 0:
                # check if end of object
                # read all properties
                propName, prop = readPropFromFile(filePointer)
                if propName != "" and propName != '}':
                    newObject.addProp(propName, prop.Value)
                else:
                    EndOfObject = 1

        ######
        # Control print
        # if objectType != 'Options':
        #     test=newObject.PropList
        #     if 'Name' in test:
        #         objName=test['Name']
        #     else:
        #         objName='None'
        #     if newObject.type != 'Block' and 'MCU' not in newObject.type  and newObject.type != 'Vehicle':
        #         print("new Object : ID= {0}, type = {1}, Name ={2}".format(test['Index'], newObject.type, objName))

    return newObject

#####################################################################################
def readGroupFromFile(filePointer, currentlevel:int, mission):
    """Read object from opened file """
    objectType = getBegining(filePointer)
    if objectType == '':
        criticalError(UNABLE_TO_FIND_OBJECT_BEGINING + str(filePointer))
    elif objectType != GROUP:
        criticalError(EXPECTED_GROUP_NOT_FOUND.format(objectType, str(filePointer)))
    else:
        #process group create object
        newGroup = AllObject()
        newGroup.type=GROUP
        #skip {
        line=readLine(filePointer)
        # read 3 lines name, index, Desc
        for i in range(3):
            propName, prop = readPropFromFile(filePointer)
            #set offsetfor group Index to avoid overlapping with objects Index
            if propName == 'Index':
                prop.Value = GROUPOFFSET+prop.Value
            newGroup.addProp(propName, prop.Value)
        #read and create objects
        endOfGroup = 0
        while endOfGroup == 0 :
            # Read kind of next entry (object or group)
            last_pos = filePointer.tell()
            objectType = getBegining(filePointer)
            filePointer.seek(last_pos)
            if objectType == '':
                endOfGroup = 1
                #skip last '{'
                line = readLine(filePointer)
            elif objectType != GROUP:
                newObject=readObjectFromFile(filePointer)
                mission.addObject(newObject, currentlevel + 1)
                newGroup.addObject(newObject.getKv(INDEX))
            else:
                #recurvivelly process groups
                subGroup=readGroupFromFile(filePointer, currentlevel + 1, mission)
                #mission.AddGroup(subGroup)
                newGroup.addObject(subGroup.getKv(INDEX))
                #line=readLine(filePointer)
                mission.addObject(subGroup, currentlevel)
        #mission.AddGroup(newGroup,currentlevel)
        mission.addObject(newGroup, currentlevel)

    return newGroup

#####################################################################################
def readLine(filePointer):
    """ read line with skipping empty lines or comment lines"""
    emptyLine=0
    while emptyLine == 0:
        line = filePointer.readline()
        # skip comment line
        m = re.search(r"\s*#", line)
        if m:
            line = filePointer.readline()
        else:
            # if line ='' => EOF
            if line == '':
                emptyLine = 1
            else:
                #skip blank lines
                m = re.search(r"^\s*$", line)
                if m:
                    #line = filePointer.readline()
                    emptyLine = 0
                else:
                    emptyLine = 1
    return (line)

#####################################################################################
def getBegining(filePointer):
    """Read the file untill the beginning of a new object"""
    error = 0
    objectName = ""
    ObjectNotFound=1
    while ObjectNotFound :
        line = readLine(filePointer)
        newObject = re.search(r"^\s*(?P<name>\w*)\s*$", line)
        EndObject = re.search(r"^\s*}\s*$", line)
        if ';' in line or line == "":
            error=1
            ObjectNotFound=0
        elif EndObject:
            objectName=''
            ObjectNotFound = 0
        elif newObject:
            objectName= newObject.group('name')
            ObjectNotFound=0
        # else:
        #     m = re.search(r"^\s*(?P<name>\w*)\s*$",line)
        #     if m:
        #         objectName= m.group('name')
        #         ObjectNotFound=0

    return objectName