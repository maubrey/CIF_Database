# Group Structure Database and Reduced Cell Search

This directory stores all of our published and unpublished .cif files in varying states of completeness. Hopefully with everything in one place (even the really bad structures) we will have an exhaustive list of every structure we have in a searchable format. 


## Installation

**Don't run these scripts from the group backup drive. Copy and paste this folder to your favorite location on your own computer.**

1. Download and install the 2020 version of the CSD along with the python API. Install the python API using either pip or conda

### Pre-requisites

**Python 3.7** and Installation of the CCDC Python API (2019)

#### Get the files
1. download the cif_database_viewer from gitlab.
2. extract the files and put them in the folder of your choice
3. Add the `database_files/` folder from the `HK Data/CIF_Database/supporting` directory on the group drive to the same folder as this `Readme.md`

#### update file paths

1. Open `python/config.json` in a text editor and update the file paths for `python_path/bin/activate` to the location of your CCDC python API which you did either through pip or conda.  
2. Update the path to the `cif_repository`  in `python/config.json` to the wherever the group drive is mounted on your computer.

#### Install required packages

In you CCDC virtual environment install `dash` and `pandas`. 
* [Pandas](https://pandas.pydata.org) is a python standard for datatables 
* [Dash](https://plotly.com) builds the web-GUI

## Running the program

Activate your CCDC virtural env and run `python app.py`


## Minimal Functionality
The script `structure_database_robust.py` will build a database of the lab's cif files using only the Python standard library and export the data to a csv. Reduced cell search is currently not implemented. 



