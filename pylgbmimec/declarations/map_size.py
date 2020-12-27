''' define here map size to be used to indexing (speedup object searching) and default coord. for object creation'''
map_size=dict()
map_size['lapino']={'XMin':0.0, 'ZMin':0.0, 'XMax':51200.0, 'ZMax':51200.0}
map_size['stalingrad']={'XMin':0.0, 'ZMin':0.0, 'XMax':230400.0, 'ZMax':358400.0}
map_size['moscow']={'XMin':0.0, 'ZMin':0.0, 'XMax':281600.0, 'ZMax':281600.0}
map_size['novosokolniki']={'XMin':0.0, 'ZMin':0.0, 'XMax':51200.0, 'ZMax':51200.0}
map_size['vluki']={'XMin':0.0, 'ZMin':0.0, 'XMax':102400.0, 'ZMax':166400.0}
map_size['kuban']={'XMin':0.0, 'ZMin':0.0, 'XMax':358395.0, 'ZMax':460800.0}
map_size['prokhorovka']={'XMin':0.0, 'ZMin':0.0, 'XMax':166400.0, 'ZMax':166400.0}
map_size['rheinland']={'XMin':0.0, 'ZMin':0.0, 'XMax':384000.0, 'ZMax':460800.0}
map_size['arras']={'XMin':0.0, 'ZMin':0.0, 'XMax':166400.0, 'ZMax':166400.0}

''' number of lines and row for the x/Z indexing'''
SPLIT_MAP = 3