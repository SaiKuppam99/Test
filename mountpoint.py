import hvac

def list_paths_and_secrets(mount_point, path):
    # Create a Vault client object
    client = hvac.Client(url='https://vault.example.com', token='<your-token>')

    # List the available paths in the secret engine
    list_response = client.secrets.kv.v2.list_secrets(mount_path=mount_point, path=path)
    keys = list_response['data']['keys']

    # Separate paths and secrets
    paths = []
    secrets = []
    for key in keys:
        if key.endswith('/'):
            paths.append(key)
        else:
            secrets.append(key)

    # Check if there are any secrets under each path
    for p in paths:
        list_response = client.secrets.kv.v2.list_secrets(mount_path=mount_point, path=path + p)
        if list_response['data']['keys']:
            secrets.append(p)
        else:
            paths.append(p)

    # Return the paths and secrets as a tuple
    return paths, secrets

# Example usage
mount_point = 'TASK'
path = 'hvac'
paths, secrets = list_paths_and_secrets(mount_point, path)
print(f"Paths: {paths}")
print(f"Secrets: {secrets}")
