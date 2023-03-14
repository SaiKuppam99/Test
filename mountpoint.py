import hvac

def list_secret_engine_paths(mount_point, path):
    """
    Lists the available paths in a Vault secret engine.
    """
    client = hvac.Client(url='https://vault.example.com', token='<your-token>')
    list_response = client.secrets.kv.v2.list_secrets(mount_path=mount_point, path=path)
    keys = list_response['data']['keys']
    paths = []
    for key in keys:
        if key.endswith('/'):
            paths.append(key)
    return paths

def list_secret_engine_secrets(mount_point, path):
    """
    Lists the available secrets in a Vault secret engine.
    """
    client = hvac.Client(url='https://vault.example.com', token='<your-token>')
    list_response = client.secrets.kv.v2.list_secrets(mount_path=mount_point, path=path)
    keys = list_response['data']['keys']
    secrets = []
    for key in keys:
        if not key.endswith('/'):
            secrets.append(key)
    return secrets

def list_secret_engine_paths_and_secrets(mount_point, path):
    """
    Lists the available paths and secrets in a Vault secret engine.
    """
    client = hvac.Client(url='https://vault.example.com', token='<your-token>')
    list_response = client.secrets.kv.v2.list_secrets(mount_path=mount_point, path=path)
    keys = list_response['data']['keys']
    paths = []
    secrets = []
    for key in keys:
        if key.endswith('/'):
            paths.append(key)
        else:
            secrets.append(key)
    for p in paths:
        list_response = client.secrets.kv.v2.list_secrets(mount_path=mount_point, path=path + p)
        if list_response['data']['keys']:
            secrets.append(p)
        else:
            paths.append(p)
    return paths, secrets

from lib import vault

mount_point = 'TASK'
path = 'hvac'

# List the available paths in the secret engine
paths = vault.list_secret_engine_paths(mount_point, path)
print(f"Paths: {paths}")

# List the available secrets in the secret engine
secrets = vault.list_secret_engine_secrets(mount_point, path)
print(f"Secrets: {secrets}")

# List the available paths and secrets in the secret engine
paths, secrets = vault.list_secret_engine_paths_and_secrets(mount_point, path)
print(f"Paths: {paths}")
print(f"Secrets: {secrets}")
