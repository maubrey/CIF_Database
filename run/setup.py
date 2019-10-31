import sys, json, os

with open('./config.json', 'r') as filehandle:
    data = filehandle.read()
data = json.loads(data.replace('\\', '/'))
PYTHON_ACTIVATE = data['python_path/bin/activate']

if sys.platform not in ['win32', 'cygwin']:
    if sys.argv[1] == 'PYTHON_PATH':
        print PYTHON_ACTIVATE
else:
    if sys.argv[1] == 'PYTHON_ACTIVATE':
        print(PYTHON_ACTIVATE)
    if sys.argv[1] == 'PYTHON_PATH':
        ppath = os.path.dirname(PYTHON_ACTIVATE)
        print os.path.join(*ppath.split('/')[:-1])
    
