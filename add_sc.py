import json
import hvac

def add_secrets_to_vault(json_file_path, vault_token):
    # Load the JSON file
    with open(json_file_path, 'r') as f:
        secrets = json.load(f)

    # Connect to the Vault server
    client = hvac.Client(url='https://your-vault-server-url.com', token=vault_token)

    # Write the secrets to the Vault
    for secret in secrets:
        path = 'secret/TASK/' + secret['User Account']
        data = {'password': secret['Password']}
        client.secrets.kv.v2.create_or_update_secret(path=path, secret=data)

    # Disconnect from the Vault server
    client.logout()
