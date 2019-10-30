ECHO ON

REM A batch script to run app.py chance path to 



python setup.py PYTHON_PATH > Output
SET /p PYTHON_PATH=<Output
SET PATH=%PATH%;%PYTHON_PATH%
ECHO %PYTHON_PATH%
python setup.py PYTHON_ACTIVATE > Output 
SET /p Python_Act=<Output
call %Python_Act%
ECHO %Python_Act%

python structure_database_robust.py
PAUSE