import sys, json

with open('./config.json', 'r') as filehandle:
    data = filehandle.read()
data = json.loads(data)
PYTHON_PATH = data['python_path/bin/activate']

if sys.argv[1] == 'PYTHON_PATH':
    print PYTHON_PATH

    
