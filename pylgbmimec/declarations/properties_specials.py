""" to trace exception or direct usage in properties handling and ease evolution/ debugging """
WARNING_LEVEL = 0

ONREPORTS = 'OnReports'
ONREPORT = 'OnReport'
ONEVENTS = 'OnEvents'
ONEVENT = 'OnEvent'
LINKTRID = 'LinkTrId'
MISOBJID = 'MisObjID'
INDEX = 'Index'
LCNAME = 'LCName'
LCDESC = 'LCDesc'
OBJECTSCRIPT = 'ObjectScript'
TARGETS ='Targets'
OBJECTS = 'Objects'
NAME = 'Name'
GUIMAP ='GuiMap'
OPTIONS = 'Options'
GROUP = 'Group'
XPOS = 'XPos'
YPOS = 'YPos'
ZPOS = 'ZPos'
YORI = 'YOri'
TYPE = 'Type'
CMDID = 'CmdId'
TARID = 'TarId'
DESC = 'Desc'
TIME = 'Time'
OBJECTS ='Objects'
WINDLAYERS = 'WindLayers'
COUNTRIES = 'Countries'
COUNTRY = 'Country'
CARRIAGES = 'Carriages'
BOUNDARY = 'Boundary'
AILEVEL = 'AILevel'
COOPSTART = 'CoopStart'
SPOTTER = 'Spotter'
PLANE = 'Plane'
PLANES = 'Planes'
AIRFIELD = 'Airfield'
MISSIONTYPE = 'MissionType'
DEATHMATCH = 2
ENABLED = 'Enabled'
COALITIONS = 'Coalitions'
SPEED = 'Speed'
ICONID = 'IconId'
LINETYPE = 'LineType'
RCOLOR = 'RColor'
GCOLOR = 'GColor'
BCOLOR = 'BColor'
LCTEXT='LCText'
STARTINAIR = 'StartInAir'
MODEL = 'Model'
SCRIPT = 'Script'
VEHICLE = 'Vehicle'
MCUWAYPOINT = 'MCU_Waypoint'
MCUCOUNTER = 'MCU_Counter'
MCUTIMER = 'MCU_Timer'
MCUDELETE = 'MCU_Delete'
MCUBEHAVIOUR = 'MCU_CMD_Behaviour'
MCUCTRIGGER ='MCU_TR_ComplexTrigger'
MCUDEACTIVATE = 'MCU_Deactivate'
MCUACTIVATE = 'MCU_Activate'
MCUTAKEOFF = 'MCU_CMD_TakeOff'
MCUICON = 'MCU_Icon'
MCUBEGIN = 'MCU_TR_MissionBegin'
MULTIPLAYERPLANECONFIG = 'MultiplayerPlaneConfig'
MCUCMDCOVER = 'MCU_CMD_Cover'
MCUTR = 'MCU_TR_Entity'
MCULAND = 'MCU_CMD_Land'
MCUMISSION ='MCU_TR_NextMission'
MCUENDMISSION = 'MCU_TR_MissionEnd'
MCUSUBTITLE ='MCU_TR_Subtitle'
MCUCMDEFFECT = 'MCU_CMD_Effect'
MCUMISSIONBEGIN = 'MCU_TR_MissionBegin'
EFFECT = 'Effect'
SUBTITLEINFO = 'SubtitleInfo'
WAYPOINTICONID = 901
ACTIONICONID = 902
EVENTENTER = 58
EVENTTOOKOFF = 66
#  FOR LANGAGE FILE
DEFAULTEXTENSION = '.eng'
LANGAGEEXTENSION = ['.chs', '.fra', '.ger', '.pol', '.rus', '.spa']
# SPECIAL PROCESSING NEEDED BECAUSE PROPERTIES HAVE SPECIAL FORMAT
LIST_OF_STRINGS=(WINDLAYERS, COUNTRIES , CARRIAGES, BOUNDARY)
DUPLICATE_CTRIGGER = [COUNTRY,OBJECTSCRIPT]
COMPLEXTRIGGERCOMMONPROP = [INDEX,NAME,'Desc',TARGETS, OBJECTS, XPOS, 'YPos', ZPOS, 'XOri', 'YOri', 'ZOri']
# FAKE PROPERTIE USE BY MIMEC
LISTNAME="LIST_NAME;"
EXCEPTION_FOR_FILTER = ['FromPoint']

