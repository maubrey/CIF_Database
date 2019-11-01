# Group Structure Database and Reduced Cell Search

This directory stores all of our published and unpublished .cif files in varying states of completeness. Hopefully with everything in one place (even the really bad structures) we will have an exhaustive list of every structure we have in a searchable format. 


## Installation

**Don't run these scripts from the group backup drive. Copy and paste this folder to your favorite location on your own computer.**

1. Download the 2019 version of the CSD. It may work with newer versions but CCDC has a habit of breaking things. 

### Windows
Pre-requisites: **Python 2.7** and Installation of the CCDC Python API (2019)

#### Get the files
1. download the cif_database_viewer from github
2. extract the files and put them in the folder of your choice
3. Add the `database_files/` folder from the `HK Data/CIF_Database/Supporting` directory on the group drive to the same folder as this file `Readme.md`

#### update file paths

1. Open `run/config.json` in a text editor and update the file paths for `python_path/bin/activate` to the location of `CCDC/Python_API_2019/miniconda/condabin/activate` which is likely in your `Program Files (x86)` directory. 
2. Also, update the path to the `cif_repository`  in `run/config.json` to the wherever the group drive is mounted on your computer.
3. In the `/run` directory you may need to right click on each `.py`: `file --> properties --> (bottom of window "Security:") []unblock` and check "unblock"
3. open and run `install_dependencies.bat`. This will pip install the necessary python modules in the CSD miniconda environment (dash and pandas). 


### Installation on MacOS/Linux
Pre-requisites: **Python 2.7** and Installation of the CCDC Python API

#### Get the files 
1. download the cif_database repository from github
2. extract the files and put them in the folder of your choice
3. In the same folder as the `run` folder, add the `database_files/` folder from the `CIF_Database/Supporting` directory on the group drive

#### update file paths
1. Confirm the path to`/Applications/CCDC/Python_API_2019/miniconda/bin/activate` and the *group database* are correct in `run/config.json`.
2. In the terminal run `bash install_dependencies.sh` 


## Running the program

###  Windows

1. Open `run.bat` (you may get a window with a security warning, click More Info then run anyway)
2. If it doesn't work make sure the file paths here are the same as in install_dependencies.bat
3. Once it is loaded go to the IP address in any web browser

### Linux and MacOS

#### From the shell script

1. In the terminal, go to this folder/run/. 
2. run `chmod a+x run.sh`
3. double click the `run.sh` icon in Finder to run. 

#### Start from a bash Terminal
1. In the terminal `source <absolute path to the ccdc python api>/miniconda/bin/activate`
2. Run ` python app.py` in terminal to start the webserver and go to the local IP address it tells you to in the browser

## Minimal Functionality
The script `structure_database_robust.py` will build a database of the lab's cif files using only the Python 2.7 standard library and also export the data to a csv. These can be quickly run using the `run_minimal.bat`  and `run_minimal.sh` files or by running the python script on its own.

## If the location of the database moves
Open `config.json` and change the path to whatever your path to the HKDATA database is. 

