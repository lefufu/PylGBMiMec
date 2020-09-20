# PylGBMiMec
**Py**thon I**l**2 **G**reat **B**attle **Mi**ssion **Mec**hanic

# What is Pyl2GB MiMec ?
A python library to automatize some painfull processes in IL2 GB mission creation.
The IL2 mission editor is powerfull, but the mechanics of mission involve creation of lot of "MCU" and link (target, object, OnReports, OnEvents,...) between objects that make things quite complicated, especially if you want to modify/update mission. The group feature is powerfull but may be aslo cumbersome if you want to update things that are spared between groups.
The mid term target of MiMec is to remove as most as possible MCU and link creation of the 3D editor, and put all the mission logic into python program.
Currently it will allow you to load a mission, search and modify by lot any mission objects then save the mission into a new one.
The following use case can be already done with few python lines:
> change height of some objects (planes, vehicle, blocks, Waypoint) by adding 50m for example.
> set country of all block around a given position or an object
> update Complex Trigger to replace planes/vehicules scripts and country (usefull if you import AA group that were not design for the plane of the current mission)  

# Main functions
## Read mission file
**readMissionFromFile** : load any IL2 GB .Mission file and reference it as an object containing all missions objects
> eg : readMissionFromFile(newMission,"D:\\jeux\\IL-2 Sturmovik Great Battles\\data\\Missions\\MyMission.Mission")
## Select Objects in Mission
**findObject** : returns a list of object fullfilling criteria given as parameters
>eg findObject(newMission, Type='Block', XPos=range(29875,29880), ZPos=range(57210, 57215))

**findObjectInRange** : return object around another object given in parameter for a given range and criteria
>eg findObjectInRange(newMission, blockTarget, Range=200, Type='Block')
## Modify Objects
**modify_kv** : modify keys given in parameters with according values given also in parameters

>Some values may be pragma function that provide values based on object properties, like adding a constant value to Ypos of each object of the list.

>Some values may be range (mix,max)

>eg modify_kv(newMission, plane1, XPos=changedX, AILevel=1, Name=changedName, Enabled=0,Country=CountryID['Germany'])

**add_in_targetList** : add a list of object as "target" for another list of objects
>eg add_target(myMission, wingmen, leaderPlane)

**set_as_targetList** : set a list of object as "target" for another list of objects, overwrite the exising "target" list
>eg set_as_target(myMission, wingmen, leaderPlane)

**add_in_objectList** : add a list of object as "object" for another list of objects
>eg add_in_objectList(myMission, WayPoints, leaderPlane)

**set_as_objectList** : set a list of object as "object" for another list of objects, overwrite the exising "object" list
>eg set_as_objectList(myMission, WayPoints, leaderPlane)

**add_OnReports** : add report, command and target to existing reports for a list of objects
> reports names are defined for 'planes', 'vehicle','Aerostat', 'ship'
> eg add_OnReports(newMission, vehicle, 'OnTargetAttacked', MCU_CMD_AttackTarget, counter)

**set_OnReports** : set report, command and target for a list of objects. Existing reports are erased.
> reports names are defined for 'planes', 'vehicle', 'Aerostat', 'ship'
> eg set_OnReports(newMission, vehicle, 'OnTargetAttacked', MCU_CMD_AttackTarget, counter)

**add_OnEvents** : add event, command and target to existing reports for a list of objects
> events names are defined for 'planes', 'vehicle','Aerostat', 'ship' and 'MCU_TR_ComplexTrigger' 
> eg add_OnEvents(newMission, flightGreen, 'OnPlaneBingoMainMG', MCU_CMD_RTB)

**set_OnEvents** : set event, command and target for a list of objects. Existing reports are erased.
> event names are defined for 'planes', 'vehicle','Aerostat', 'ship' and 'MCU_TR_ComplexTrigger' 
> eg set_OnEvents(newMission, flightGreen, 'OnPlaneBingoMainMG', MCU_CMD_RTB)

**add_ObjScriptList** : add models (scripts) and countries to "script list" of a complex MCU trigger
> a table is given to add Countries by their names instead of their number
> if only country or script is used, only the corresponding part will be modified
> eg set_ObjScriptList(newMission, ctrigger, ObjScriptList=['luascripts\\worldobjects\\planes\\bf109g4.txt', 'luascripts\\worldobjects\\planes\\p40e1.txt'])

**set_ObjScriptList** : set models (scripts) and countries to "script list" of a complex MCU trigger. Existing scripts and countries are erased
> if only country or script is used, only the corresponding part will be modified
eg set_ObjScriptList(newMission, ctrigger, Countries=[CountryID['United States'], CountryID['Germany']])

## View objects
**scanObjectList** : return as sting some properties, given in parameter, of a list of object. It can be printed by command print for debugging/control purpose.
> eg print(scanObjectList(newMission, ctrigger, 'Name', 'Type', 'LinkTrId','ObjectScript','Country'))

## Save Mission
**saveMission** : save the results of all operations into a new mission, given by tis name. 
> The name can be a full path (eg F:\game\IL2\data\Missions\MyMission.Mission) but "\" must be doubled
> All localization files (.eng, .fra,..) of the original mission will be copied accordingly to the new name.
> eg saveMission(newMission,"D:\\jeux\\IL-2 Sturmovik Great Battles\\data\\Missions\\test_mini.Mission")
# how to install / use
Donwload and install python 3.x from [python.org](https://www.python.org/downloads/windows/)
