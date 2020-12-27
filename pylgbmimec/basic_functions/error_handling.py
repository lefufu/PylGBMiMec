# message definition here
UNABLE_TO_FIND_OBJECT_BEGINING = "Error : Unable to read object from file"
UNABLE_TO_READ_OBJECT_FROM_FILE = "Error : Unable to read object from file:"
CAN_NOT_READ_PROPERTIE = "Error : Can not read propertie : format not supported. Line = "
CAN_NOT_READ_LIST_PROPERTIE = "Error : Can not read list propertie : list not started correctly. Prop.name ={0}"
INVALID_TARGET_TYPE = "Error : Bad format for adding target : \"{0}\" for object: {1}"
INVALID_OBJECT_TYPE = "Error : Bad format for adding object : \"{0}\" for object: {1}"
CAN_NOT_CLONE_PROPERTIE = "Error : Can not clone propertie: {0}"
EXPECTED_GROUP_NOT_FOUND = "Error : Group was expected but not found in line \"{0}\" of file {1}."
MISSION_FILE_WITHOUT_OPTION = "Error : Mission file not started with \"Options\" object"
CAN_NOT_OPEN_FILE = "Error : Can not open file: \"{0}\""
CAN_NOT_WRITE_FILE = "Error : Can not open file for writing : \"{0}\""
MAP_NOT_FOUND = "Error : Map not declared : \"{0}\""
INVALID_TYPE_FOR_RANGE = "Error : Propertie data type {0} not compliant with filter {1}={2} on object {3}"
BAD_FILTER_RANGE ="Error : Invalid Range filter : {0}"
DOUBLE_RANGE_FILTER = "Error : FromPoint can not be used in findObjectInRange function"
CAN_NOT_MODIFY_INDEX = "Error : Can not modify Index for object {0}"
REPORT_NOT_DEFINED_FOR_TYPE = "Error : Report not defined for type {0}"
EVENT_NOT_DEFINED_FOR_TYPE = "Error : Event not defined for type {0}"

""" handle error """
def criticalError(message):
    raise Exception(message)
