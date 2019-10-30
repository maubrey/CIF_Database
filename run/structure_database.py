#! C:\Program Files (x86)\CCDC\Python_API_2019\miniconda\python2.7
from ccdc.io import EntryReader, EntryWriter
from ccdc.entry import Entry
from ccdc.crystal import CellAngles, CellLengths
from ccdc.search import TextNumericSearch, ReducedCellSearch
import os, sys, hashlib, re, json
#######
config_file_path = './config.json'
#######

with open(config_file_path, 'r') as filehandle:
    data = filehandle.read()
data = json.loads(data.replace('\\', '\\\\'))
DATABASE_PATH =  data['cif_repository'].replace('\\', '/')
json_database_path = data['json_database_path'].replace('\\', '/')
csdsql_database_path = data['csdsql_database_path'].replace('\\', '/')
json_search_results_path = data['json_search_results_path'].replace('\\', '/')
csv_export_path = data['csv_export_path'].replace('\\', '/')

def get_csd_entries_by_author(author):
    '''
    Uses the default csd databases based on the version of the python API this is being used
    conducts a search
    returns list of refcodes
    '''
    query = TextNumericSearch()
    query.add_author(author)
    return [h.identifier for h in query.search()]

def get_entry(identifier):
    '''
    input an identifier as a string and get the
    ccdc.entry.Entry object
    '''
    csd_reader = EntryReader('CSD')
    entry = csd_reader.entry(identifier)
    return entry

def get_entries(identifiers):
    '''
    input a list of identifiers and return a list of ccdc.entry.Entry objects
    '''
    entries = [get_entry(i) for i in identifiers]
    return entries


def get_labs_published_cifs(author):
    '''
    input an author's name and save all of their cifs to a
    folder in DATABASE_PATH
    '''
    published_data = get_csd_entries_by_author(author)
    entries = get_entries(published_data)

    folder_name =  author.replace('.', '')
    directory = os.path.join(os.getcwd(), ('cifs/'+ folder_name + '_CSD/'))
    if os.path.isdir(directory): 
        pass
    else: os.mkdir(directory)
    cnt = 1
    for entry in entries:
        with EntryWriter(directory+entry.identifier+'.cif') as filehandle:
            filehandle.write(entry)
        string = str(cnt) + ' Files Saved to ' + directory
        sys.stdout.write("\r" + string)
        sys.stdout.flush()
        cnt+=1
    print ('\n')


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

def parse_cifs(list_of_paths):
    '''
    extracts important information about the structures
    outputs all the data as a list of dictionaries

    options: 
    max_lines: limits the amount of the cif that is read since we don't need all of the hkl data here
    '''
    search_terms = {
            '_audit_creation_date': r'(_audit_creation_date)\s*(\d\d\d\d-\d\d-\d\d)',
            '_database_code_CSD':r'(_database_code_CSD)\s*(\S*)\n',
            '_publ_author_name': r'(_publ_author_name)\s*([^_]*)\n(?<!p)[l_]',
            '_chemical_formula_moiety':r'(_chemical_formula_moiety)\s*([^_]*)\n(?<!p)[l_]',
            '_journal_paper_doi': r'(_journal_paper_doi)\s*([^_]*)\n(?<!p)[l_]',
            '_chemical_name_common':r'(_chemical_name_common)\s*([^_]*)\n(?<!p)[l_]',
            '_diffrn_ambient_temperature':r'(_diffrn_ambient_temperature)\s*([^_]*)\n(?<!p)[l_]',
            '_refine_ls_R_factor_gt':r'(_refine_ls_R_factor_gt)\s*([^_]*)\n(?<!p)[l_]' ,       
            '_refine_ls_wR_factor_gt':r'(_refine_ls_wR_factor_gt)\s*([^_]*)\n(?<!p)[l_]' ,     
            '_diffrn_radiation_probe':r'(_diffrn_radiation_probe)\s*([^_]*)\n(?<!p)[l_]'  ,     
            '_diffrn_source':r'(_diffrn_source)\s*([^_]*)\n(?<!p)[l_]'  ,              
            '_symmetry_cell_setting':r'(_symmetry_cell_setting)\s*([^_]*)\n(?<!p)[l_]' ,     
            '_symmetry_space_group_name_H-M':r'(_symmetry_space_group_name_H-M)\s*([^_]*)\n(?<!p)[l_]',
            '_space_group_name_H-M_alt':r'(_space_group_name_H-M_alt)\s*([^_]*)\n(?<!p)[l_]',
            '_symmetry_Int_Tables_number':r'(_symmetry_Int_Tables_number)\s*([^_]*)\n(?<!p)[l_]',   
            '_space_group_name_Hall' :r'(_space_group_name_Hall)\s*([^_]*)\n(?<!p)[l_]' ,      
            '_cell_length_a' :r'(_cell_length_a)\s*([^_]*)\n(?<!p)[l_]' ,            
            '_cell_length_b' :r'(_cell_length_b)\s*([^_]*)\n(?<!p)[l_]' ,            
            '_cell_length_c' :r'(_cell_length_c)\s*([^_]*)\n(?<!p)[l_]' ,            
            '_cell_angle_alpha' :r'(_cell_angle_alpha)\s*([^_]*)\n(?<!p)[l_]' ,         
            '_cell_angle_beta' :r'(_cell_angle_beta)\s*([^_]*)\n(?<!p)[l_]' ,          
            '_cell_angle_gamma' :r'(_cell_angle_gamma)\s*([^_]*)\n(?<!p)[l_]' ,         
            '_cell_volume' :r'(_cell_volume)\s*([^_]*)\n(?<!p)[l_]' ,              
            '_exptl_crystal_colour' :r'(_exptl_crystal_colour)\s*([^_]*)\n(?<!p)[l_]' ,     
            '_exptl_crystal_description' :r'(_exptl_crystal_description)\s*([^_]*)\n(?<!p)[l_]' ,
            '_cell_formula_units_Z'   :r'(_cell_formula_units_Z)\s*([^_]*)\n(?<!p)[l_]' ,   
            #Advanced Refinement data
            '_cell_measurement_reflns_used':r'(_cell_measurement_reflns_used)\s*([^_]*)\n(?<!p)[l_]' ,   
            '_cell_measurement_temperature' :r'(_cell_measurement_temperature)\s*([^_]*)\n(?<!p)[l_]' ,  
            '_cell_measurement_theta_max' :r'(_cell_measurement_theta_max)\s*([^_]*)\n(?<!p)[l_]' ,    
            '_cell_measurement_theta_min' :r'(_cell_measurement_theta_min)\s*([^_]*)\n(?<!p)[l_]' ,    
            '_exptl_absorpt_correction_type':r'(_exptl_absorpt_correction_type)\s*([^_]*)\n(?<!p)[l_]' , 
            '_exptl_absorpt_process_details':r'(_exptl_absorpt_process_details)\s*([^_]*)\n(?<!p)[l_]' ,
            '_exptl_crystal_density_diffrn':r'(_exptl_crystal_density_diffrn)\s*([^_]*)\n(?<!p)[l_]' ,
            '_exptl_crystal_density_meas' :r'(_exptl_crystal_density_meas)\s*([^_]*)\n(?<!p)[l_]' , 
            '_exptl_crystal_density_method':r'(_exptl_crystal_density_method)\s*([^_]*)\n(?<!p)[l_]' ,
            '_exptl_crystal_F_000' :r'(_exptl_crystal_F_000)\s*([^_]*)\n(?<!p)[l_]' ,        
            '_exptl_crystal_recrystallization_method':r'(_exptl_crystal_recrystallization_method)\s*([^_]*)\n(?<!p)[l_]' ,
            '_exptl_special_details':r'(_exptl_special_details)\s*([^_]*)\n(?<!p)[l_]' ,

            '_diffrn_measured_fraction_theta_full':r'(_diffrn_measured_fraction_theta_full)\s*([^_]*)\n(?<!p)[l_]' , 
            '_diffrn_measured_fraction_theta_max':r'(_diffrn_measured_fraction_theta_max)\s*([^_]*)\n(?<!p)[l_]' , 
            '_diffrn_measurement_device_type' :r'(_diffrn_measurement_device_type)\s*([^_]*)\n(?<!p)[l_]' ,    
            '_diffrn_measurement_method'   :r'(_diffrn_measurement_method)\s*([^_]*)\n(?<!p)[l_]' ,       
            '_diffrn_radiation_type' :r'(_diffrn_radiation_type)\s*([^_]*)\n(?<!p)[l_]' ,             
            '_diffrn_radiation_wavelength' :r'(_diffrn_radiation_wavelength)\s*([^_]*)\n(?<!p)[l_]' ,       

            '_refine_diff_density_max' :r'(_refine_diff_density_max)\s*([^_]*)\n(?<!p)[l_]' ,        
            '_refine_diff_density_min' :r'(_refine_diff_density_min)\s*([^_]*)\n(?<!p)[l_]' ,        
            '_refine_diff_density_rms' :r'(_refine_diff_density_rms)\s*([^_]*)\n(?<!p)[l_]' ,        
            '_refine_ls_extinction_coef' :r'(_refine_ls_extinction_coef)\s*([^_]*)\n(?<!p)[l_]' ,      
            '_refine_ls_goodness_of_fit_ref':r'(_refine_ls_goodness_of_fit_ref)\s*([^_]*)\n(?<!p)[l_]' , 
            '_refine_ls_number_parameters' :r'(_refine_ls_number_parameters)\s*([^_]*)\n(?<!p)[l_]' ,   
            '_refine_ls_number_reflns' :r'(_refine_ls_number_reflns)\s*([^_]*)\n(?<!p)[l_]' ,       
            '_refine_ls_number_restraints' :r'(_refine_ls_number_restraints)\s*([^_]*)\n(?<!p)[l_]' ,           
 

            '_refine_special_details':r'(_refine_special_details)\s*([^_]*)\n(?<!p)[l_]' ,
            '_olex2_refinement_description':r'(_olex2_refinement_description)\s*([^_]*)\n(?<!p)[l_]' ,
            '_space_group_crystal_system':r'(_space_group_crystal_system)\s*([^_]*)\n(?<!p)[l_]' ,
        }
    parsed = [] #init the output list
    for path in list_of_paths:  #get the data as text and its hash
        path = path.replace('\\', '/')
        entry = dict()
        entry['path']=os.path.normpath(path)
        entry['hash']=hash_file(path)

        filename_pattern = re.compile(DATABASE_PATH + r'/([^/]*)')
        entry['parent'] = filename_pattern.search(path).group(1)
        print entry['parent']
       #build regex and find first entry for every thing
       #should be robust logic to handle all search terms
        with open(path, 'rt') as filehandle:
            data = filehandle.read()
        for item in search_terms:
            pattern = re.compile(search_terms[item])
            result = pattern.search(data)
            try:
                if result == None: 
                    entry[item] = ''
                else:
                    entry[item] = pattern.search(data).group(2)
            except: entry[item] = ''
        parsed.append(entry)
    return parsed

def cleanup_parsed_cifs(cif_dict):
    '''cleans up the formatting of some of the data entries'''
    out = []
    for cif in cif_dict:
        cif['_cell_length_a'] = cif['_cell_length_a'].split('(')[0]
        cif['_cell_length_b'] = cif['_cell_length_b'].split('(')[0]
        cif['_cell_length_c'] = cif['_cell_length_c'].split('(')[0]
        cif['_cell_volume'] = cif['_cell_volume'].split('(')[0]
        cif['_cell_angle_alpha'] = cif['_cell_angle_alpha'].split('(')[0]
        cif['_cell_angle_beta'] = cif['_cell_angle_beta'].split('(')[0]
        cif['_cell_angle_gamma'] = cif['_cell_angle_gamma'].split('(')[0]

        cif['_symmetry_space_group_name_H-M'] = cif['_symmetry_space_group_name_H-M'].replace(' ', '').replace('\'', '')
        if cif['_space_group_name_H-M_alt'] != "" and cif['_symmetry_space_group_name_H-M'] == "":
            cif['_symmetry_space_group_name_H-M'] = cif['_space_group_name_H-M_alt'].replace(' ', '').replace('\'', '')

        if cif['_symmetry_cell_setting'] == "":
            cif['_symmetry_cell_setting'] = cif['_space_group_crystal_system'].replace('\'', '')
        
        out.append(cif)
    return out

def parsed_cifs_2_json(parsed_cifs, filename=json_database_path):
    '''
    input "parsed cifs" as a list of dictionaries
    output a json file (default output filename is json_database_path)
    '''
    parsed_cifs = json.dumps(parsed_cifs)
    with open(filename, 'w') as writer:
        writer.write(parsed_cifs)
    return parsed_cifs

def update_databases():
    cifs = get_all_cifs()
    parsed = parse_cifs(cifs)
    parsed_cifs_2_json(cleanup_parsed_cifs(parsed))
    entries = []
    for i in cifs:
        entries.append(cif_2_entry(i))
    entries_2_database(entries)
    

def cif_2_entry(filepath): 
    '''
    input a file path to .cif
    and return a ccdc.entry.Entry object
    '''
    with open(filepath, 'r') as cif_file:
        cif = cif_file.read()
        new_entry = Entry.from_string(cif)

        #this just makes sure there is a unique identifier for every entry
        # hash file to use as identifier
        if new_entry.ccdc_number == None:
            new_entry.identifier = hash_file(filepath)

    return new_entry


def entries_2_database(entry_list, output_file=csdsql_database_path): #broken
    '''
    input a list of entry objects and ouput a csdsql file
    '''

    with EntryWriter(output_file) as filehandle:
        for entry in entry_list:
            try: filehandle.write(entry)
            except RuntimeError as e: 
                print str(e)
                if str(e).startswith('CSDSQLDatabase::append():'): print 'dulplicate file found'
                continue
    return 'csdsql file updated.'
        


def hash_file(path):
    hasher = hashlib.sha1()
    with open(path, 'rt') as filehandle:
        data = filehandle.read()
        while len(data) > 0:
            hasher.update(data)
            data = filehandle.read() #BLOCKSIZE if slow
    cif_hash =  hasher.hexdigest()
    return cif_hash


def my_reduced_cell_search(user_a, user_b, user_c, 
                            user_alpha, user_beta, user_gamma, user_centring, 
                            database=csdsql_database_path, filename=json_search_results_path,
                            length_tolerance = 1.5, angle_tolerance=2.0):
    # lattice_centring_dict = {
    #                 'P':'primitive','C':'C-centred','F':'F-centred','I':'I-centred',
    #                 'R':'R-obverse','?':'unknown centring','B':'B-centred','A':'A-centred'}
    
    #build the search
    query = ReducedCellSearch.Query(CellLengths(a=user_a, b=user_b, c=user_c),
                            CellAngles(alpha=user_alpha, beta=user_beta, gamma=user_gamma),
                            user_centring)
    searcher=ReducedCellSearch(query=query,)
    searcher.settings.absolute_angle_tolerance= float(length_tolerance)
    searcher.settings.percent_length_tolerance = float(angle_tolerance)
    hits = searcher.search(database=database) #/inhouse.csdsql

    #load in the cif database as a list of dictionaries
    with open(json_database_path, 'r') as filehandle:
        data = filehandle.read()
    data = json.loads(data)

    search_results = [] # the list of dicts to export as json
    for h in hits:
        for i in data:
            if i['hash'] == h.identifier:
                print i['hash']
                search_results.append(i)
            elif i['_database_code_CSD'] == h.identifier:
                print h.identifier
                search_results.append(i)
    parsed_cifs_2_json(search_results, filename='../database_files/search_results.json')

    print(str(len(hits)) + ' hits found.')


if __name__ == '__main__':

    update_databases()
    # my_reduced_cell_search(24.1, 16.7, 8.5, 90, 90, 90, 'primitive', length_tolerance=50, angle_tolerance=25)







