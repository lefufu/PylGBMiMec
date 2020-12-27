from basic_functions.error_handling import criticalError, REPORT_NOT_DEFINED_FOR_TYPE, EVENT_NOT_DEFINED_FOR_TYPE

""" definition of event name and ID to ease their use"""

event_name=dict()
event_name['Plane']={
    0: 'OnPilotKilled',
    1: 'OnPilotWounded',
    2: 'OnPlaneCrashed',
    3: 'OnPlaneCriticalDamage',
    4: 'OnPlaneDestroyed',
    5: 'OnPlaneLanded',
    6: 'OnPlaneTookOff',
    7: 'OnPlaneBingoFuel',
    8: 'OnPlaneBingoMainMG',
    9: 'OnPlaneBingoBombs',
    10: 'OnPlaneBingoTurrets',
    11: 'OnPlaneGunnersKilled',
    12: 'OnDamaged',
    13: 'OnKilled',
    15: 'OnMovedTo',
    20: 'OnPlaneSpawned',
    21: 'OnOutOfPlanes',
    22: 'OnPlaneAdded',
    23: 'OnFlagBlocked',
    24: 'OnFlagUnblocked',
    25: 'OnFlagCapturedBy00',
    26: 'OnFlagCapturedBy01',
    27: 'OnFlagCapturedBy02',
    28: 'OnFlagCapturedBy03',
    29: 'OnFlagCapturedBy04',
    30: 'OnFlagCapturedBy05',
    31: 'OnFlagCapturedBy06',
    32: 'OnFlagCapturedBy07',
    33: 'OnFlagCapturedBy08',
    34: 'OnFlagCapturedBy09',
    35: 'OnFlagCapturedBy10',
    36: 'OnFlagCapturedBy11',
    37: 'OnFlagCapturedBy12',
    38: 'OnFlagCapturedBy13',
    39: 'OnFlagCapturedBy14',
    40: 'OnFlagCapturedBy15',
    41: 'OnFlagCapturedBy16',
    74: 'OnSpottingStarted',
    79: 'OnPlaneBingoCargo'
}
event_name['Aerostat']={
    0: 'OnPilotKilled',
    1: 'OnPilotWounded',
    2: 'OnPlaneCrashed',
    3: 'OnPlaneCriticalDamage',
    4: 'OnPlaneDestroyed',
    5: 'OnPlaneLanded',
    6: 'OnPlaneTookOff',
    7: 'OnPlaneBingoFuel',
    8: 'OnPlaneBingoMainMG',
    9: 'OnPlaneBingoBombs',
    10: 'OnPlaneBingoTurrets',
    11: 'OnPlaneGunnersKilled',
    12: 'OnDamaged',
    13: 'OnKilled',
    15: 'OnMovedTo',
    74: 'OnSpottingStarted',
    79: 'OnPlaneBingoCargo'
}
event_name['Vehicle']={
    12: 'OnDamaged',
    13: 'OnKilled',
    15: 'OnMovedTo',
    74: 'OnSpottingStarted'
}
event_name['Ship']={
    12: 'OnDamaged',
    13: 'OnKilled',
    15: 'OnMovedTo',
    74: 'OnSpottingStarted'
}
event_name['MCU_TR_ComplexTrigger']={
    57:'OnObjectSpawned',
    58:'OnObjectEnteredSimple',
    59:'OnObjectEnteredAlive',
    60:'OnObjectLeft',
    61:'OnObjectLeftAlive',
    62:'OnObjectFinished',
    63:'OnObjectFinishedAlive',
    64:'OnObjectStationaryAndAlive',
    65:'OnObjectFinishedStationaryAndAlive',
    66:'OnObjectTookOff',
    67:'OnObjectDamaged',
    68:'OnObjectCriticallyDamaged',
    69:'OnObjectRepaired',
    70:'OnObjectKilled',
    71:'OnObjectDropedBombs',
    72:'OnObjectFiredRockets',
    73:'OnObjectFiredFlare',
    75:'OnObjectDroppedCargoContainers',
    76:'OnObjectDeliveredCargo',
    77:'OnObjectParatrooperJumped',
    78:'OnObjectParatrooperLandedAlive'
}

def findEvent(typeObj:str, eventName:str):
    """ Find report number by entering object type and report name
    :param typeObj: str
        object type
    :param eventName: str
        name of event
    """
    foundNum=-1

    if typeObj not in event_name:
        criticalError(EVENT_NOT_DEFINED_FOR_TYPE.format(typeObj))

    for eventNum in event_name[typeObj]:
        if event_name[typeObj][eventNum] == eventName:
            foundNum = eventNum

    return foundNum

""" Filter associated with Event in complex triggers"""
filter_CTRIGGER=dict()
filter_CTRIGGER={
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
    73:'EventsFilterFiredFlare',
    75:'EventsFilterDroppedCargoContainers',
    76:'EventsFilterDeliveredCargo',
    77:'EventsFilterParatrooperJumped',
    78:'EventsFilterParatrooperLandedAlive'
}