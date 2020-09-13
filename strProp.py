#####################################################################################
from declarations.properties_specials import LIST_OF_STRINGS, OBJECTSCRIPT, LISTNAME, COUNTRY


def StrProp(propertieName: str, propValue: object) -> str:
    """ convert a propertie into the format used in mission file"""
    convert2str = propertieName
    typeProp = type(propValue)
    # UNITARY
    if typeProp == float or typeProp == int:
        convert2str += " = {0};".format(propValue)
    if typeProp == str:
        convert2str += " = {0};".format(propValue)
    # ARRAYS
    if typeProp == set:
        tempStr = str(propValue)
        if len(propValue) != 0:
            tmpStr = tempStr.replace('{', '[').replace('}', ']') + ";"
            if tmpStr == "[\'\'];":
                tmpStr= '[];'
        else:
            tmpStr = '[];'
        convert2str += " = " + tmpStr


    # DICTIONNARY
    if typeProp == dict:
        convert2str += "\n{"
        for lvalue in propValue:
            if lvalue != LISTNAME:
                convert2str += "\n  {0} = {1};".format(lvalue, propValue[lvalue])
        convert2str += "\n}"
    # LIST
    if typeProp == list:
        if propertieName != OBJECTSCRIPT and propertieName != COUNTRY :
            convert2str += "\n{"
            #if propertieName == 'WindLayers' or propertieName == 'Countries' or propertieName == 'Carriages':
            if propertieName in LIST_OF_STRINGS:
                convert2str += "\n"
            for i in range(len(propValue)):
                #if propertieName != 'WindLayers' and propertieName != 'Countries' and propertieName != 'Carriages':
                if propertieName not in LIST_OF_STRINGS:
                    tmp="\n"+StrProp(propValue[i].Value[LISTNAME],propValue[i].Value)
                else:
                    tmp = propValue[i].Value
                convert2str += tmp
            #if propertieName != 'WindLayers' and propertieName != 'Countries'and propertieName != 'Carriages':
            if propertieName not in LIST_OF_STRINGS:
                convert2str += "\n}"
            else:
                convert2str += "}"
        else:
            # handle multiple "ObjectScript" or "country" lines for complex MCU
            convert2str=""
            for pval in propValue:
                convert2str += propertieName+" = "+str(pval)+";\n"
    return convert2str