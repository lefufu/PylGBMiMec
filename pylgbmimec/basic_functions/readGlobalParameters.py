import json

def initialize_variables_from_file(file_path):

    with open(file_path, 'r') as file:
        PWCGsettings = json.load(file)
        return (PWCGsettings)
