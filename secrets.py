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


def write_secret(secret, cluster_name):
    """
    Writes the given secret to a file with the format <cluster_name>-<key>-secret.
    """
    secret_path = secret['path']
    secret_data = secret['data']['data']
    with open('secrets.txt', 'a') as f:
        for key, value in secret_data.items():
            key_name = f"{cluster_name}-{key}-secret"
            f.write(f"{key_name}: {value}\n")

