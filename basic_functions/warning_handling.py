# message definition here
PROP_NOT_EXISTING = "Warning : propertie name {0} not existing for object {1}, criterion can not be fullfill"
ONLY_FIRST_OBJECT_USED = "Warning : only first object of list {0} will be used as center for findObjectInRange()"
PROP_TO_MODIFY_NOT_EXISTS = "Warning : property {0} to modify in object {1}:{2} is not existing"
PROP_TO_MODIFY_WRONG_FORMAT = "Warning : property {0} to modify in object {1}:{2} as not the same format as new value; {3} instead of {4}"
DUPLICATE_PROPERTIE = "Warning : Duplicate entry for same propertie : {0} for object ID {1}"
EMPTY_CENTER = "Warning : Empty center for FromPoint, criterion can not be fullfill"
ENTITY_NOT_LINKED = "Warning : Object {0} has not linked entity, operation {1} can not be fullfilled"
TYPE_NOT_SUPPORTED_FOR_REQUEST = "Warning : type {0} not supported for request on {1}"
PROP_NOT_EXISTING_FOR_MOD = "Warning : propertie name {0} not existing for object {1}, modification can not be fullfill"
""" handle warning_msg """
def warning_msg(message):
    print(message)