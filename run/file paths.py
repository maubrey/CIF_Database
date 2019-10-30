import json, csv, os
#######
config_file_path = './config.json'
#######

with open(config_file_path, 'r') as filehandle:
    data = filehandle.read()
data = json.loads(data)
DATABASE_PATH =  data['cif_repository']
json_database_path = data['json_database_path']
csdsql_database_path = data['csdsql_database_path']
json_search_results_path = data['json_search_results_path']
csv_export_path = data['csv_export_path']


def get_all_cifs(dirpath=DATABASE_PATH):
    '''
    returns a list of all cif files in the directory 
    and all subdirectories that are provided
    '''
    cif_paths = []
    parent = []
    for root, dirs, files  in os.walk(dirpath):
        parent.append(dirs)
        for name in files:
            if name.endswith('.cif'):
                relative_path =  os.path.join(root, name)
                cif_paths.append(relative_path)
    return cif_paths


test = '..\database_files\inhouse.json'
print os.path.normcase(test)
print os.path.abspath(test)
print os.path.basename(test)
