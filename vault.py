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



cmd = ['vault', 'kv', 'list', '-format=json', 'TAS-EU']
try:
    output = subprocess.check_output(cmd)
except subprocess.CalledProcessError as e:
    print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
    print("Output:\n", e.output.decode())
    exit(1)

# Parse the JSON output into a Python object
try:
    result = json.loads(output)
except ValueError as e:
    print("Error decoding JSON output:", e)
    print("Output:\n", output.decode())
    exit(1)

