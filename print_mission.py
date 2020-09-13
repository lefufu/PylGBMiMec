from basic_handling.error_handling import *
from basic_handling.mission_class import Mission, StrProp, offset
from basic_handling.object_class import AllObject

#header and footer to add in mission file
from declarations.country import CountryName
from declarations.properties_specials import NAME, INDEX, DESC, GROUP, COUNTRY

HEADER = "# Mission File Version = 1.0;\n"
FOOTER = "\n# end of file"
# ---------------------------------------------
def printObject(mobject:AllObject, filepointer):
    """ print contain of a group in console or in file """
    lines = str(mobject)+"\n"
    if filepointer:
        filepointer.write(lines)
    else:
        print(lines)

# ---------------------------------------------
def printGroup(group:AllObject, mission:Mission, filepointer):
    """ print contain of a group in console or in file """
    fileflag=0
    begin = offset(group)
    # Group Header
    line=group.type+'\n{\n'
    line+=begin+StrProp(NAME, group.PropList[NAME])+'\n'
    line +=begin+StrProp(INDEX, group.PropList[INDEX])+'\n'
    line +=begin+ StrProp(DESC, group.PropList[DESC])+'\n'
    if filepointer:
        filepointer.write(line)
    else:
        print(line)
    #group contain
    for iobj in sorted(group.getKv('Objects')):
        obj=mission.ObjList[iobj]
        if obj.type == 'Group':
            printGroup(obj, mission, filepointer)
            line = "\n}"
        else:
            printObject(obj, filepointer)
            line = "}\n"


    if filepointer:
        filepointer.write(line)
    else:
        print(line)
# ---------------------------------------------
def printMission(mission:Mission, filename: str = ''):
    """ print contain of a mission in console or in file """
    #TODO : copy .eng files
    outputfile = None
    fileflag = 0
    if filename != '':
        outputfile = open(filename, 'w')
        outputfile.write(HEADER)
        if not outputfile:
            CriticalError(CAN_NOT_WRITE_FILE.format(filename))
        fileflag = 1

    # process all level 0 objects
    for obj in sorted(mission.ObjList) :
        mobjet=mission.ObjList[obj]
        if mobjet.Level == 0:
            # process objects
            if mobjet.type != GROUP:
                printObject(mobjet, outputfile)
            else:
                #process group
                printGroup(mobjet, mission, outputfile)

    if fileflag:
        outputfile.write(FOOTER)
        outputfile.close()

    return

# ---------------------------------------------
def scanObjectList(mission:Mission, objectList: list, *properties):
    """ convert into string properties information of a list of objects """
    convert2str=''
    for index in objectList:
        # create an object by cloning current object and its linked entity if any
        currentObj = mission.ObjList[index].cloneWithLinkedEntityProp(0, mission)
        currentObj.type = mission.ObjList[index].type
        convert2str += '\n ID:'+str(index)+", Type = "+currentObj.type
        for prop in properties:
            if prop in currentObj.PropList:
                propval = currentObj.PropList[prop]
                if prop == COUNTRY:
                    if type (propval) != list :
                        #replace number by country name
                        propval="'"+CountryName[propval]+"'"
                    else:
                        # replace all elements by country name
                        result=[]
                        for countryID in propval:
                            result.append(CountryName[countryID])
                        propval=result
                convert2str += ", "+str(prop)+"="+str(propval)

    return convert2str