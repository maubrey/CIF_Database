ECHO ON

REM A batch script to install dependancies needed to view the database 


python setup.py PYTHON_PATH > Output
SET /p PYTHON_PATH=<Output
SET PATH=%PATH%;%PYTHON_PATH%
ECHO %PYTHON_PATH%
python setup.py PYTHON_ACTIVATE > Output 
SET /p Python_Act=<Output
call %Python_Act%
ECHO %Python_Act%


pip install dash==1.4.1
pip install pandas
PAUSE