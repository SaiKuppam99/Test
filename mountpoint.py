import hvac

def connect_to_vault(url, token):
    client = hvac.Client(url=url, token=token)
    return client

def get_paths_and_secrets(client, mount_point):
    paths = []
    secrets = []
    list_response = client.secrets.kv.v2.list_secrets(
        mount_path=mount_point
    )
    for key in list_response['data']['keys']:
        if key.endswith('/'):
            paths.append(key)
        else:
            secrets.append(key)
    return paths, secrets

def check_if_secret_exists(client, mount_point, secret_path):
    response = client.secrets.kv.v2.read_secret_version(
        mount_point=mount_point,
        path=secret_path
    )
    if 'data' in response:
        return True
    else:
        return False
