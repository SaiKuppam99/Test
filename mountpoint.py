import hvac

def list_secrets_and_paths(mount_point, client):
    secrets = []
    paths = []

    # List all secrets and paths under the given mount point
    secrets_response = client.secrets.kv.v2.list_secrets(
        mount_point=mount_point,
        path='',
    )
    secrets_list = secrets_response['data']['keys']
    for item in secrets_list:
        if item.endswith('/'):
            paths.append(item)
        else:
            secrets.append(item)

    # List latest version of each secret
    for secret in secrets:
        secret_metadata_response = client.secrets.kv.v2.read_metadata(
            mount_point=mount_point,
            path=secret
        )
        latest_version = secret_metadata_response['data']['latest_version']
        secrets[secrets.index(secret)] = "{} (latest version: {})".format(secret, latest_version)

    return (paths, secrets)


from function.secrets import list_secrets_and_paths
import hvac

client = hvac.Client(
    url='https://my-vault-server.com:8200',
    token='<your-token>'
)

mount_point = 'mysecrets'

paths, secrets = list_secrets_and_paths(mount_point, client)

print("Paths in the '{}' mount point:".format(mount_point))
for path in paths:
    print("- {}".format(path))

print("Secrets in the '{}' mount point:".format(mount_point))
for secret in secrets:
    print("- {}".format(secret))
