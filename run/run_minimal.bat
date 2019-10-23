ECHO ON

REM A batch script to run app.py chance path to 
SET PATH=%PATH%;C:\PROGRA~2\CCDC\PYTHON~2\MINICO~1\
call C:\PROGRA~2\CCDC\PYTHON~2\MINICO~1\condabin\activate
chdir ..
python structure_database.py
PAUSE