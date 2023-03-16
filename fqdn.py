import hvac
import os

def get_secrets(vault_addr, token, folder):
    """
    Recursively reads all the secrets inside the given folder in HashiCorp Vault
    and writes the fully qualified names of the secrets to a file named values.txt.
    """
    # Create the bin directory if it doesn't exist
    bin_dir = os.path.join(os.getcwd(), 'bin')
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)

    # Open the values file for writing
    values_path = os.path.join(bin_dir, 'values.txt')
    with open(values_path, 'w') as f:
        # Connect to the Vault server
        client = hvac.Client(url=vault_addr, token=token)

        # Recursively read the secrets inside the folder
        _get_secrets(client, folder, f)

def _get_secrets(client, folder, f, prefix=""):
    """
    Recursively reads all the secrets inside the given folder in HashiCorp Vault
    and writes the fully qualified names of the secrets to the given file handle.
    """
    # List the items in the folder
    try:
        items = client.secrets.kv.v2.list_secrets(path=folder)['data']['keys']
    except:
        return

    # Iterate over the items
    for item in items:
        item_path = os.path.join(folder, item)

        # Check if the item is a folder or a secret
        if item.endswith('/'):
            # If it's a folder, recursively read the secrets inside it
            _get_secrets(client, item_path, f, prefix + item)
        else:
            # If it's a secret, add its fully qualified name to the file
            f.write(prefix + item + '\n')


# Example usage:
vault_addr = 'http://localhost:8200'
token = 'my_vault_token'
folder = 'secret'
get_secrets(vault_addr, token, folder)
