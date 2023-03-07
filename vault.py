import subprocess

cmd = ['vault', 'kv', 'list', '-format=json', 'TAS-EU']
output = subprocess.check_output(cmd)

# Parse the JSON output into a Python object
result = json.loads(output)

# Extract the list of keys and folders from the output
keys = [k for k in result['data']['keys'] if not k.endswith('/')]
folders = [f.rstrip('/') for f in result['data']['keys'] if f.endswith('/')]

# Print the list of keys and folders
print('Keys:')
print('-----')
for key in keys:
    print(key)

print('\nFolders:')
print('--------')
for folder in folders:
    print(folder)



import subprocess

cmd = ['vault', 'kv', 'list', 'TAS-EU']
output = subprocess.check_output(cmd).decode('utf-8')

# Extract the list of keys from the output
keys_str = output.strip().split('\n')[1:]
keys = [int(key) for key in keys_str if not key.endswith('/')]

# Print the list of keys
print('Keys:')
print('-----')
for key in keys:
    print(key)
======================================================================
keys = ['deployment/', 'test', 'config/', 'scripts']

# Create empty lists to store the values
paths = []
values = []

# Iterate through the keys and split them into paths and values
for key in keys:
    if key.endswith('/'):
        paths.append(key)
    else:
        values.append(key)

# Print the resulting lists
print('Paths:', paths)
print('Values:', values)


