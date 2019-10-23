# Karunadasa Group Structure Database and Reduced Cell Search

This directory stores all of our published and unpublished .cif files in varying states of completeness. Hopefully with everything in one place (even the really bad structures) we will have an exhaustive list of every structure we have in a searchable format. 

This program can effectively to all of these except *notebook number* which is hopefully in the filename of working data 

## Installation

**Don't run these scripts from the group backup drive. Copy and paste this folder to your favorite location on your own computer.**

1. Download the 2019 version of the CSD. It may work with newer versions but CCDC has a habit of breaking things. 

### Windows
1. install the CSD python API 
2. open  `install_dependancies.bat` in text editor and confirm the files paths to where CSD python API  is installed. If step 3 doesn't work then these paths are probably wrong
3. run `install_dependancies.bat` as **administrator**
4. this batch file will install the necessary python modules in the CSD miniconda environment



### Installation on MacOS/Linux
1. In the terminal `source <absolute path to the ccdc python api>/miniconda/bin/activate`. For example `/Applications/CCDC/Python_API_2019/miniconda/bin/activate`
2. `pip install dash==1.4.1`
3. `pip install pandas`
4.  Run app.py
5. Confirm the path to`/Applications/CCDC/Python_API_2019/miniconda/bin/activate` in run.sh is correct

## Running the program

###  Windows

1. open `run.bat`
2. if it doesn't work make sure the file paths here are the same as in install_dependancies.bat

### Linux

#### From the shell script

1. In the terminal, go to this folder. 
2. `chmod a+x run.sh`
3. you can now just double click the icond to run. 
4. Alternatively,  on MacOs,  you have have the script run via an Automator quick action (optional).

#### Start from terminal
1. In the terminal `source <absolute path to the ccdc python api>/miniconda/bin/activate`
2. Run ` python app.py` in terminal to start the webserver and go to the local IP address it tells you to in the browser


## Minimal Build

The script `structure_database_robust.py` will build a database of the lab's cif files without using only the Python 2.7 standard libaray. These can be quickly run using the `run_minimal.` bat and sh files or by running the python script as main. 

## If the location of the database moves

Open `config.json` and change the path to whatever your path to the HKDATA database is. 

