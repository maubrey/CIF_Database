ECHO OFF

REM A batch script to run app.py run the SET Path command it this isn't working
REM SET PATH=%PATH%;C:\PROGRA~2\CCDC\PYTHON~2\MINICO~1\



python setup.py PYTHON_PATH > Output
SET /p PYTHON_PATH=<Output
SET PATH=%PATH%;%PYTHON_PATH%
ECHO %PYTHON_PATH%
python setup.py PYTHON_ACTIVATE > Output 
SET /p Python_Act=<Output
call %Python_Act%
ECHO %Python_Act%
python app.py
PAUSE