import hvac
import os

def read_secrets_file(file_path):
    """
    Reads the list of secrets from a file.
    """
    with open(file_path, 'r') as f:
        secrets = [line.strip() for line in f]
    return secrets

def get_secret(client, secret_path):
    """
    Gets the value of a secret from Vault.
    """
    secret_version = client.secrets.kv.v2.read_secret_version(path=secret_path)
    if secret_version is not None and 'data' in secret_version and 'data' in secret_version['data']:
        return secret_version['data']['data']
    return {}

def write_secrets_file(secrets, file_path):
    """
    Writes the key-value pairs of secrets to a file.
    """
    with open(file_path, 'w') as f:
        for secret_path in secrets:
            secret = get_secret(client, secret_path)
            for key, value in secret.items():
                f.write(f"{secret_path}:{key}={value}\n")

# Example usage:
vault_addr = 'http://localhost:8200'
token = 'my_vault_token'
secrets_file = 'secrets.txt'
secrets = read_secrets_file(secrets_file)

# Connect to the Vault server
client = hvac.Client(url=vault_addr, token=token)

# Write the key-value pairs of secrets to a file
secrets_values_file = 'secrets_values.txt'
write_secrets_file(secrets, secrets_values_file)


import os

def modify_key_name(secret_file_path, cluster_name):
    # Create a new file to write the modified lines
    new_file_path = os.path.join(os.getcwd(), 'bin', f'{cluster_name}-secrets.txt')
    with open(new_file_path, 'w') as new_file:
        # Open the secrets file for reading
        with open(secret_file_path, 'r') as f:
            # Read each line and modify the key name
            for line in f:
                key, value = line.strip().split('=')
                new_key = f'{cluster_name}-{key}-secret'
                new_line = f'{new_key}: {value}\n'
                # Write the modified line to the new file
                new_file.write(new_line)
    
    return new_file_path


