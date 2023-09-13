''' define here map size to be used to indexing (speedup object searching) and default coord. for object creation'''
map_size=dict()
map_size['lapino']={'XMin':0.0, 'ZMin':0.0, 'XMax':51200.0, 'ZMax':51200.0}
map_size['stalingrad']={'XMin':0.0, 'ZMin':0.0, 'XMax':230400.0, 'ZMax':358400.0}
map_size['moscow']={'XMin':0.0, 'ZMin':0.0, 'XMax':281600.0, 'ZMax':281600.0}
map_size['novosokolniki']={'XMin':0.0, 'ZMin':0.0, 'XMax':51200.0, 'ZMax':51200.0}
map_size['vluki']={'XMin':0.0, 'ZMin':0.0, 'XMax':102400.0, 'ZMax':166400.0}
map_size['kuban']={'XMin':35370,  'ZMin':35285, 'XMax':323145.0, 'ZMax':450920.0}
map_size['prokhorovka']={'XMin':0.0, 'ZMin':0.0, 'XMax':166400.0, 'ZMax':166400.0}
map_size['rheinland']={'XMin':30077, 'ZMin':29953, 'XMax':354045.0, 'ZMax':430845.0}
map_size['arras']={'XMin':30000, 'ZMin':30000, 'XMax':136385.0, 'ZMax':136340.0}
map_size['normandy-summer']={'XMin':25000, 'ZMin':30000.0, 'XMax':371775.0, 'ZMax':340895.0}
map_size['western_front']={'XMin':32015, 'ZMin':32015.0, 'XMax':313595.0, 'ZMax':390400.0}

''' number of lines and row for the x/Z indexing'''
SPLIT_MAP = 3