""" to trace exception or direct usage in properties handling and ease evolution/ debugging """
ONREPORTS = 'OnReports'
ONREPORT = 'OnReport'
ONEVENTS = 'OnEvents'
ONEVENT = 'OnEvent'
LINKTRID = 'LinkTrId'
INDEX = 'Index'
OBJECTSCRIPT = 'ObjectScript'
TARGETS ='Targets'
OBJECTS = 'Objects'
NAME = 'Name'
GUIMAP ='GuiMap'
OPTIONS = 'Options'
GROUP = 'Group'
XPOS = 'XPos'
ZPOS = 'ZPos'
TYPE = 'Type'
CMDID = 'CmdId'
TARID = 'TarId'
DESC = 'Desc'
OBJECTS ='Objects'
WINDLAYERS = 'WindLayers'
COUNTRIES = 'Countries'
COUNTRY = 'Country'
CARRIAGES = 'Carriages'
MULTIPLAYERPLANECONFIG = 'MultiplayerPlaneConfig'
# SPECIAL PROCESSING NEEDED BECAUSE PROPERTIES HAVE SPECIAL FORMAT
LIST_OF_STRINGS=(WINDLAYERS, COUNTRIES , CARRIAGES)
DUPLICATE_CTRIGGER = [COUNTRY,OBJECTSCRIPT]
COMPLEXTRIGGERCOMMONPROP = [INDEX,NAME,'Desc',TARGETS, OBJECTS, XPOS, 'YPos', ZPOS, 'XOri', 'YOri', 'ZOri']
# FAKE PROPERTIE USE BY MIMEC
LISTNAME="LIST_NAME;"
EXCEPTION_FOR_FILTER = ['FromPoint']
