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

    
    def add_secrets_to_vault(json_file):
    with open(json_file) as f:
        secrets = json.load(f)

    for secret in secrets:
        path = 'TASK/' + secret['User Name']
        data = {'username': secret['User Name'], 'password': secret['Password']}
        
        # check if secret already exists
        existing_secret = client.secrets.kv.v1.read_secret(mount_point='secret', path=path)
        if existing_secret is None:
            # secret does not exist, create it
            client.secrets.kv.v1.create_or_update_secret(mount_point='secret', path=path, secret=data)
            print(f"Created new secret at path {path}")
        else:
            # check if the existing secret needs to be updated
            needs_update = False
            if 'data' not in existing_secret or existing_secret['data'] != data:
                # data has changed
                needs_update = True
                
            if 'metadata' in secret and secret['metadata'] != existing_secret['metadata']:
                # metadata has changed
                needs_update = True
            
            if needs_update:
                # update the secret
                client.secrets.kv.v1.create_or_update_secret(mount_point='secret', path=path, secret=data)
                print(f"Updated secret at path {path}")
            else:
                # secret exists and has not been modified
                print(f"Secret at path {path} already exists and has not been modified")
