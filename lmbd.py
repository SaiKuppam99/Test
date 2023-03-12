import hvac
import boto3
from datetime import datetime, timedelta

VAULT_ADDR = "https://example.com:8200"
VAULT_TOKEN = "s.abc123def456ghi789"
VAULT_PATH = "secret/data/my/path"
PROJECT_NAME = "my_project"
ENVIRONMENT = "dev"


def main():
    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

    if client.sys.is_sealed():
        print("Vault is sealed")
        return
    else:
        print("Vault is unsealed")

    secrets_data = get_secrets_data(client, VAULT_PATH)

    new_secrets_data = modify_secret_keys(PROJECT_NAME, ENVIRONMENT, secrets_data)

    write_to_secret_manager(new_secrets_data)


def get_secrets_data(client, path):
    secrets = client.secrets.kv.v2.list_secrets(path=path)
    directories = []
    secrets_data = {}
    for secret in secrets["data"]["keys"]:
        if secret.endswith("/"):
            directories.append(secret[:-1])
        else:
            secret_data = client.secrets.kv.v2.read_secret_version(path=path+"/"+secret)["data"]["data"]
            secret_time = datetime.strptime(secret_data["time"], '%Y-%m-%dT%H:%M:%S.%fZ')
            if datetime.utcnow() - secret_time < timedelta(hours=1):
                secrets_data[secret] = secret_data

    for directory in directories:
        sub_path = path+"/"+directory
        sub_secrets = client.secrets.kv.v2.list_secrets(path=sub_path)
        for secret in sub_secrets["data"]["keys"]:
            secret_path = sub_path+"/"+secret
            secret_data = client.secrets.kv.v2.read_secret_version(path=secret_path)["data"]["data"]
            secret_time = datetime.strptime(secret_data["time"], '%Y-%m-%dT%H:%M:%S.%fZ')
            if datetime.utcnow() - secret_time < timedelta(hours=1):
                secrets_data[directory+"/"+secret] = secret_data

    return secrets_data


def modify_secret_keys(project_name, environment, secrets_data):
    new_secrets_data = {}
    for secret_key, secret_data in secrets_data.items():
        new_secret_key = f"{project_name}-{environment}-{secret_key}-secret"
        new_secrets_data[new_secret_key] = secret_data

    return new_secrets_data


def write_to_secret_manager(secrets_data):
    client_sm = boto3.client('secretsmanager')
    for secret_key, secret_data in secrets_data.items():
        try:
            client_sm.describe_secret(SecretId=secret_key)
        except:
            client_sm.create_secret(Name=secret_key, SecretString=str(secret_data))
            print(f"New secret {secret_key} created in AWS Secret Manager")
        else:
            print(f"Secret {secret_key} already exists in AWS Secret Manager")


if __name__ == "__main__":
    main()
    
    
    

    
    
import hvac

def get_vault_secret(vault_url, vault_token, secret_path):
    # Create a client instance and authenticate with Vault
    client = hvac.Client(url=vault_url, token=vault_token)

    # Retrieve the secret from Vault
    try:
        secret = client.secrets.kv.v2.read_secret_version(path=secret_path)
        return secret["data"]["data"]
    except Exception as e:
        raise ValueError(f"Unable to retrieve secret from Vault: {str(e)}")
