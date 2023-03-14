import hvac

# Create a Vault client object
client = hvac.Client(url='https://vault.example.com', token='<your-token>')

# Define the mount point you want to check
mount_point = 'my-secret'

# List the paths under the mount point
paths = client.secrets.kv.v2.list_secrets(path=mount_point)['data']['keys']
if paths:
    print(f"The following paths are under {mount_point}:")
    for path in paths:
        print(f"- {path}")
        # List any secrets under each path
        secrets = client.secrets.kv.v2.read_secret_version(path=f"{mount_point}/{path}")['data']['data']
        if secrets:
            print(f"The following secrets are under {mount_point}/{path}:")
            for key, value in secrets.items():
                print(f"- {key}: {value}")
        else:
            print(f"There are no secrets under {mount_point}/{path}.")
else:
    print(f"There are no paths under {mount_point}.")
