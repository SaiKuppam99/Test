import hvac
import os

def get_secrets(vault_addr, token, folder, secrets_file):
    """
    Recursively reads all the secrets inside the given folder in HashiCorp Vault
    and writes them to a file named secrets_file inside a bin directory.
    """
    # Create the bin directory if it doesn't exist
    bin_dir = os.path.join(os.getcwd(), 'bin')
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)

    # Open the secrets file for writing
    secrets_path = os.path.join(bin_dir, secrets_file)
    with open(secrets_path, 'w') as f:
        # Connect to the Vault server
        client = hvac.Client(url=vault_addr, token=token)

        # Recursively read the secrets inside the folder
        secrets = _get_secrets(client, folder)

        # Write the secrets to the file
        for secret in secrets:
            f.write(secret + '\n')

def _get_secrets(client, folder):
    """
    Recursively reads all the secrets inside the given folder in HashiCorp Vault.
    """
    secrets = []

    # List the items in the folder
    items = client.secrets.kv.v2.list_secrets(path=folder)['data']['keys']

    # Iterate over the items
    for item in items:
        item_path = os.path.join(folder, item)

        # Check if the item is a folder or a secret
        if client.secrets.kv.v2.read_secret_version(path=item_path)['data'] is not None:
            # If it's a secret, add its value to the list
            secret = client.secrets.kv.v2.read_secret_version(path=item_path)['data']['data']['value']
            secrets.append(secret)
        else:
            # If it's a folder, recursively read the secrets inside it
            secrets.extend(_get_secrets(client, item_path))

    return secrets

# Example usage:
vault_addr = 'http://localhost:8200'
token = 'my_vault_token'
folder = 'secret/project'
secrets_file = 'secrets.txt'
get_secrets(vault_addr, token, folder, secrets_file)
