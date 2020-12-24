"""template file to create MiMec file for your Mission
Version 1.0
2020/09/20, Lefuneste
See https://github.com/lefufu/PylGBMiMec/blob/master/README.md
 """
# Lines started with "#" are comment
# DO NOT MODIFY the line below, they are needed to make the python working
from basic_functions.mission_class import *
from basic_functions.find_object import *
from basic_functions.modify_object import *
from basic_functions.object_creation import copy_from_mission
from basic_functions.save_mission import *
from declarations.country import *

#You can print messages on console by using "print" command as below
print("PyL2MiMec default template")

#This entry create the variable that will contain your mission. You can replace "newMission" by the word you want, but you will have to use it in all other commands
newMission=Mission()

#testing for single player mission
#The mission is read below
#You can use full path like "D:\\jeux\\IL-2 Sturmovik Great Battles\\data\\Missions\\MyMission.Mission")
#just beware of using "\\" instead of "\" in the path
readMissionFromFile(newMission, "testing\\MyMission.Mission")

#will display a summary of the mission contain
print("Mission summary :")
print(newMission)

#example of a command that find planes using criteria and put it under the name "objlist"
# 5 objects should be returned, 3 planes and 2 MCU,  only 1 plane should have Enabled to 1, 1 plane should not display Enabled'
# the criterion on string is base on regexp expression, so all name containing "Plane" will fit
planeList=findObject(newMission, Name='Plane')

#this command will display Name, Type, LinkTrId and "Enabled" properties of each objects of planeList
print("Just to show properties of a group of objects")
print(scanObjectList(newMission, planeList, 'Name', 'Type', 'LinkTrId','Enabled'))
#we won't modify planeList, it's just an example of select and display

#let's do some modification
#this time we will select object of type plane wiht a name containing "Plane"
planeList=findObject(newMission, Name='Plane', Type='Plane')
#print its properties before modification
print("\nBefore modification:")
print(scanObjectList(newMission, planeList, 'Name', 'Type', 'LinkTrId','Country','XPos','AILevel','Enabled'))

#Let's define 2 functions :
#This one will increase 'XPos' by 10
changedX = lambda obj: obj.PropList['XPos']+10
#This one will add "_test" to the object name
changedName = lambda obj: "\""+obj.PropList['Name'].replace("\"","")+"_test"+"\""

# then we can modify plane1, we will change it's XPos and Name by using functions, and set its propertie "Enabled" to 0
# and its Country to 'Germany"
# notice that object ID29 named "Plane" does not have a linkTrId, and for the moment MiMec will not create it.
# So Enabled can not be changed
modify_kv(newMission, planeList, XPos=changedX, AILevel=1, Name=changedName, Enabled=0, Country=CountryID['Germany'])
#Display the modifications
print("\nAfter modification:")
print(scanObjectList(newMission, planeList, 'Name', 'Type', 'LinkTrId','Country','XPos','AILevel','Enabled'))

#Let's modify country for blocks that are in 900m range of a MCU attack target
#at first let's find the MCU
blockTarget = findObject(newMission, Type='MCU', Name='command Attack')
#Then find block list
block2Modify = findObjectInRange(newMission, blockTarget, Range=900, Type='Block')
#Then let's modify the country to "Germany" for these blocks
modify_kv(newMission, block2Modify, Country=CountryID['Germany'])

#Now, let's update a complex MCU scripts and country
#at first let's find the one who is using il2m41 as script (only a part of script name will work)
# As we select all obejct with type containing "MCU" and most of them does not have ObjectScript properties
# we will have warning messages
# If we have use 'ComplexTrigger' instead of 'MCU' we would have only select complex trigger, so no warning
ctrigger=findObject(newMission, Type='MCU', ObjectScript='il2m41')

#now let's overwrite its objectscript list and countries (should be set in one time, but just to show it can also be done
#for countries and scripts independantly
set_ObjScriptList(newMission, ctrigger, ObjScriptList=['luascripts\\worldobjects\\planes\\bf109g4.txt', 'luascripts\\worldobjects\\planes\\p40e1.txt'])
set_ObjScriptList(newMission, ctrigger, Countries=[CountryID['United States'], CountryID['Germany']])

#now let's import objects from another mission
#a reference mission "default_objets" with all object has been created
#to allow adding "bare" objects for future developement
#but you can import any object of another mission and put it in the new mission
#the example below is adding all object of default_objets.Mission named "*Vehicle*" into the group3 of the new mission
print("\n******************")
print('copy object features')
defautlObjects=Mission()
readMissionFromFile(defautlObjects, "declarations\\default_objets.Mission")
newID=copy_from_mission(newMission, defautlObjects, 'Group3', Name='Vehicle')
modify_kv(newMission, newID, Name='Vehicle_Copied_In_Group3' )

#now let's delete object "Plane2_test" in Group1
print("\n******************")
print('delete object features')
objlist=findObject(newMission, Type='Plane', Group='Group1', Name='Plane2_test')
deleteObject(newMission, objlist)

#Now it's time to save the mission
print('Modified mission written in \"testing\" directory as \"test_mini.Mission\". Try to load it with Mission Editor and compare it with \"MyMission.Mission\" "')
saveMission(newMission, "testing\\test_mini.Mission")


