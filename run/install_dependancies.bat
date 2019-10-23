ECHO ON

REM A batch script to install dependancies needed to view the database 
SET PATH=%PATH%;C:\PROGRA~2\CCDC\PYTHON~2\MINICO~1\
call C:\PROGRA~2\CCDC\PYTHON~2\MINICO~1\condabin\activate
pip install dash==1.4.1
pip install pandas
PAUSE