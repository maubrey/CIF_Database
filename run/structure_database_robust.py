'''
The purpose of this script is to to duplicate all of the essential 
database maintenance of structure_database.py using only Python standard 
libraries that are compatible with a Python 2 and Python 3 environment

Run as main to
1.  generate json 
2. generate csv
3. can be opened with Excel or 

'''

import os, hashlib, re, json, csv
import sys

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
        entry = dict()
        entry['path']=path
        entry['hash']=hash_file(path)
        
        entry['parent'] = path[:len(DATABASE_PATH)].split('/')[0]
        #define all the search terms here
        
       
       #build regex and find first entry for every thing
       #should be robust logic to handle all search terms
        with open(path, 'rt') as filehandle:
            data = filehandle.read()
        for item in search_terms:
            pattern = re.compile(search_terms[item])
            result = pattern.search(data)
            if result == None: 
                entry[item] = ''
            else:
                entry[item] = pattern.search(data).group(2)
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

def json_2_csv(json_file_path=json_database_path):
    
    with open(json_file_path, 'rt') as filehandle:
        data = filehandle.read()
    data = json.loads(data)

    with open(csv_export_path, "w") as filehandle:
        f = csv.writer(filehandle)

        # Write CSV Header, If you dont need that, remove this line
        columns = data[0].keys()
        f.writerow(columns)
        
        for datum in data:
            f.writerow([str(datum[o]).replace("\n", "").replace(",", "").replace('\r', '') for o in columns])

                    


def update_databases():
    cifs = get_all_cifs()
    parsed = parse_cifs(cifs)
    parsed_cifs_2_json(cleanup_parsed_cifs(parsed))

    #convert json to csv
    json_2_csv()


def hash_file(path):
    hasher = hashlib.sha1()
    with open(path, 'rt') as filehandle:
        data = filehandle.read()
        while len(data) > 0:
            hasher.update(data)
            data = filehandle.read() #BLOCKSIZE if slow
    cif_hash =  hasher.hexdigest()
    return cif_hash

if __name__ == '__main__':
    update_databases()
