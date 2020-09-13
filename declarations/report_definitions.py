from basic_handling.error_handling import CriticalError, REPORT_NOT_DEFINED_FOR_TYPE

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
report_name['MCU_TR_ComplexTrigger']={
    57:'EventsFilterSpawned',
    58:'EventsFilterEnteredSimple',
    59:'EventsFilterEnteredAlive',
    60:'EventsFilterLeftSimple',
    61:'EventsFilterLeftAlive',
    62:'EventsFilterFinishedSimple',
    63:'EventsFilterFinishedAlive',
    64:'EventsFilterStationaryAndAlive',
    65:'EventsFilterFinishedStationaryAndAlive',
    66:'EventsFilterTookOff',
    67:'EventsFilterDamaged',
    68:'EventsFilterCriticallyDamaged',
    69:'EventsFilterRepaired',
    70:'EventsFilterKilled',
    71:'EventsFilterDropedBombs',
    72:'EventsFilterFiredRockets',
    73: 'EventsFilterFiredFlare',
    75:'EventsFilterDroppedCargoContainers',
    76:'EventsFilterDeliveredCargo',
    77:'EventsFilterParatrooperJumped',
    78:'EventsFilterParatrooperLandedAlive'
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
        CriticalError(REPORT_NOT_DEFINED_FOR_TYPE.format(typeObj))

    for reportNum in report_name[typeObj]:
        if report_name[typeObj][reportNum] == reportName:
            foundNum = reportNum

    return foundNum