from ..basic_functions.error_handling import criticalError, REPORT_NOT_DEFINED_FOR_TYPE

""" definition of report name and ID to ease their use"""

report_name=dict()
report_name['Plane']={
    0:'OnSpawned',
    1:'OnTargetAttacked',
    2:'OnAreaAttacked',
    3:'OnTookOff',
    4:'OnLanded'
}
report_name['Aerostat']={
    0:'OnSpawned',
    1:'OnTargetAttacked',
    2:'OnAreaAttacked',
    3:'OnTookOff',
    4:'OnLanded'
}
report_name['Vehicle']={
    0:'OnSpawned',
    1:'OnTargetAttacked',
    2:'OnAreaAttacked'
}
report_name['Ship']={
    0:'OnSpawned',
    1:'OnTargetAttacked',
    2:'OnAreaAttacked'
}

def findReport(typeObj:str, reportName:str):
    """ Find report number by entering object type and report name
    :param typeObj: str
        object type
    :param reportName: str
        name of report
    """
    foundNum=-1

    if typeObj not in report_name:
        criticalError(REPORT_NOT_DEFINED_FOR_TYPE.format(typeObj))

    for reportNum in report_name[typeObj]:
        if report_name[typeObj][reportNum] == reportName:
            foundNum = reportNum

    return foundNum