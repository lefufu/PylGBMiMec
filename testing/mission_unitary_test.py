"""testing for mission
    Read and print group and objects from a simple mission test file
 """
#TODO deplace files in local DIRECTORY
from pylgbmimec.basic_functions.mission_class import *
from pylgbmimec.basic_functions.find_object import *
from pylgbmimec.basic_functions.modify_object import *
from pylgbmimec.basic_functions.object_creation import copy_from_mission
from pylgbmimec.basic_functions.save_mission import *
from pylgbmimec.declarations.country import *

print("test on simple mission")
newMission=Mission()
#readMissionFromFile(newMission,"D:\\jeux\\IL-2 Sturmovik Great Battles\\data\\Missions\\MyMission.Mission")
readMissionFromFile(newMission, "MyMission.Mission")
print(newMission)

print("\n******************")
print('delete object features')
objlist=findObject(newMission, Type='Plane', Group='Group1', Name='Plane2')
deleteObject(newMission, objlist)

print("\n******************")
print('copy object features')
defautlObjects=Mission()
readMissionFromFile(defautlObjects, "..\\pylgbmimec\\declarations\\default_objets.Mission")
newID=copy_from_mission(newMission, defautlObjects, 'Group3', Name='Vehicle')

print("\n******************")
print('find object by name ')
print('5 objects should be returned, 3 planes and 2 MCU\nonly 1 plane should have Enabled to 1\n 1 plane should not display Enabled')
objlist=findObject(newMission, Name='Plane')
print(scanObjectList(newMission, objlist, 'Name', 'Type', 'LinkTrId','Enabled'))

print("\n******************")
print('find object by type and Enabled ')
print('Only one object should be displayed\n1 warnig should be issued')
objlist=findObject(newMission, Type='Plane', Enabled=1)
print(scanObjectList(newMission, objlist, 'Name', 'Type', 'LinkTrId','Enabled'))

print("\n******************")
print('test to modify key/values for plane including one in linkTrId')
print('name, country, xpos and enabled should be changed')
print('Functions are used to change XPos (+10) and Name')
changedX = lambda obj: obj.PropList['XPos']+10
changedName = lambda obj: "\""+obj.PropList['Name'].replace("\"","")+"_test"+"\""
plane1=findObject(newMission, Name='Plane1')
print(scanObjectList(newMission, plane1, 'Name', 'Type', 'LinkTrId','Country','XPos','AILevel','Enabled'))
modify_kv(newMission, plane1, XPos=changedX, AILevel=1, Name=changedName, Enabled=0,Country=CountryID['Germany'])
print(scanObjectList(newMission, plane1, 'Name', 'Type', 'LinkTrId','Country','XPos','AILevel','Enabled'))

print("\n******************")
print('test on OnReport')
print('command is issued on vehicule object')
print('but assicated linked MCU should be modified')
vehicle=findObject(newMission, Name='Vehicle$', Type='Vehicle')
MCU_CMD_AttackTarget=findObject(newMission, Name='command Attack')
counter=findObject(newMission, Name='Trigger Counter')
LinkTrId=findObject(newMission, Name='Vehicle entity')
print(scanObjectList(newMission, MCU_CMD_AttackTarget, 'Name', 'LinkTrId'))
print(scanObjectList(newMission, counter, 'Name', 'LinkTrId'))
print(scanObjectList(newMission, vehicle, 'Name', 'LinkTrId','OnReports'))
print(newMission.ObjList[LinkTrId[0]])
add_OnReports(newMission, vehicle, 'OnTargetAttacked', MCU_CMD_AttackTarget, counter)
print(scanObjectList(newMission, vehicle, 'Name', 'LinkTrId','OnReports'))
print(newMission.ObjList[LinkTrId[0]])

print("\n******************")
print('play with complex trigger properties')
print('Only one object should be displayed\nsome warning should be issued')
print('Modify country and script retained for filter, keep only 2 planes and 2 countries')
ctrigger=findObject(newMission, Type='MCU', ObjectScript='bf109')
print(scanObjectList(newMission, ctrigger, 'Name', 'Type', 'LinkTrId','ObjectScript','Country'))
set_ObjScriptList(newMission, ctrigger, ObjScriptList=['luascripts\\worldobjects\\planes\\bf109g4.txt', 'luascripts\\worldobjects\\planes\\p40e1.txt'])
set_ObjScriptList(newMission, ctrigger, Countries=[CountryID['United States'], CountryID['Germany']])
print(scanObjectList(newMission, ctrigger, 'Name', 'Type', 'LinkTrId','ObjectScript','Country'))

print("\n******************")
print('write modified mission')
#saveMission(newMission,"D:\\jeux\\IL-2 Sturmovik Great Battles\\data\\Missions\\test_mini.Mission")
saveMission(newMission, "test_mini.Mission")

print("***************************************")
print("read / write big mission and select objects by coordinates")
print("modify some object in staraya reka around X=29877.51 & Z=57212.42")
print("4 objects should be found and modified")
readMissionFromFile(newMission, r"Velikiye Luki tutorial finished.Mission")
blockTarget = findObject(newMission, Type='Block', XPos=range(29875,29880), ZPos=range(57210, 57215))
block2Modify = findObjectInRange(newMission, blockTarget, Range=200, Type='Block')
print(scanObjectList(newMission, blockTarget, 'Name', 'XPos', 'Zpos', 'Country'))
print(scanObjectList(newMission, block2Modify, 'Name', 'XPos', 'Zpos', 'Country'))
modify_kv(newMission, block2Modify, Country=CountryID['Germany'])
print(scanObjectList(newMission, block2Modify, 'Name', 'XPos', 'Zpos', 'Country'))
print('write modified mission')
#saveMission(newMission,"D:\\jeux\\IL-2 Sturmovik Great Battles\\data\\Missions\\test_Vluki.Mission")
saveMission(newMission, "test_Vluki.Mission")

#testing for coop mission
print("***************************************")
print("Testing COOP Mission")
readMissionFromFile(newMission, "SYN-Coop05.Mission")
saveMission(newMission, "test_coop.Mission")