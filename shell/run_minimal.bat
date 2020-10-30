ECHO OFF

REM A batch script to run app.py chance path to 



python ../python/setup.py PYTHON_PATH > Output
SET /p PYTHON_PATH=<Output
SET PATH=%PATH%;%PYTHON_PATH%
ECHO %PYTHON_PATH%
python ../python/setup.py PYTHON_ACTIVATE > Output 
SET /p Python_Act=<Output
call :testargs "%Python_Act%"
ECHO %Python_Act%

python ../python/structure_database_robust.py
PAUSE

:testargs
call %~s1
goto :eof