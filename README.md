# PylGBMiMec
**Py**thon I**l**2 **G**reat **B**attle **Mi**ssion **Mec**hanic

# What is Pyl2GB MiMec ?
A python library to automatize some painfull processes in IL2 GB mission creation.
It will allow you to load a mission, search and modify by lot any mission objects then save the mission into a new one.

# Main functions

**readMissionFromFile** : load any IL2 GB .Mission file and reference it as an object containing all missions objects
> eg : readMissionFromFile(newMission,"D:\\jeux\\IL-2 Sturmovik Great Battles\\data\\Missions\\MyMission.Mission")

**findObject** : returns a list of object fullfilling criteria given as parameters
>eg findObject(newMission, Type='Block', XPos=range(29875,29880), ZPos=range(57210, 57215))

**findObjectInRange** : return object around another object given in parameter for a given range and criteria
>eg findObjectInRange(newMission, blockTarget, Range=200, Type='Block')

**modify_kv** : modify keys given in parameters with according values given also in parameters
>eg modify_kv(newMission, plane1, XPos=changedX, AILevel=1, Name=changedName, Enabled=0,Country=CountryID['Germany'])
Some values may be pragma function that provide values based on object properties, like adding a constant value to Ypos of each object of the list.

**


# how to install / use
to be filled
