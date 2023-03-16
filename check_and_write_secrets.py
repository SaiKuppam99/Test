import os
import hvac


def check_and_write_secrets(client, mount_path):
    # Create the bin directory if it doesn't exist
    os.makedirs('bin', exist_ok=True)

    # Read the paths from the file and iterate through them
    with open('bin/paths.txt', 'r') as f:
        for path in f.read().splitlines():
            # Check if any secrets exist at this path
            secret_response = client.secrets.kv.v2.read_secret_version(
                mount_point=mount_path,
                path=path
            )
            if 'data' in secret_response:
                # Write the secrets to a file
                with open(f'bin/{path}_secret.txt', 'w') as secret_file:
                    for key, value in secret_response['data']['data'].items():
                        secret_file.write(f'{key}={value}\n')

            # Check if any subpaths exist under this path
            list_response = client.secrets.kv.v2.list_secrets(
                mount_point=mount_path,
                path=path + '/'
            )
            if 'data' in list_response:
                # Write the subpaths to a file
                with open(f'bin/{path}_path.txt', 'w') as path_file:
                    for subpath in list_response['data']['keys']:
                        path_file.write(f'{subpath}\n')
