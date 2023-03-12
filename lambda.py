import os
import hvac

def check_vault_sealed():
    # Load Vault server URL from environment variable
    vault_url = os.environ.get('VAULT_URL')
    if not vault_url:
        raise ValueError('Vault URL not set in environment variable "VAULT_URL"')
    
    # Create a new Vault client
    client = hvac.Client(url=vault_url)
    
    # Check if Vault server is sealed
    status = client.sys.is_sealed()
    if status:
        return "Vault is sealed, please unseal the Vault"
    else:
        return "Vault is unsealed"

    
import subprocess

def check_vault(vault_url, vault_token, secret_path):
    # Check if Vault server is sealed
    sealed = subprocess.run(['vault', 'status', '-format=json'], capture_output=True)
    if sealed.returncode != 0:
        raise RuntimeError('Error checking Vault status')
    
    sealed_json = json.loads(sealed.stdout)
    if sealed_json['sealed']:
        return "Vault is sealed, please unseal the Vault"
    
    # Check if secret path exists
    path_exists = subprocess.run(['vault', 'kv', 'get', '-format=json', secret_path], 
                                 env={'VAULT_ADDR': vault_url, 'VAULT_TOKEN': vault_token},
                                 capture_output=True)
    
    if path_exists.returncode == 0:
        # Path exists, read and display output
        secret_value = json.loads(path_exists.stdout)['data']['data']
        return f"Secret value for path {secret_path}: {secret_value}"
    else:
        # Path does not exist
        return f"Path {secret_path} does not exist"
 
==========================================================================================================
    
import subprocess

def check_vault(vault_url, vault_token, secret_path):
    # Check Vault status
    status = subprocess.run(['vault', 'status'], 
                            env={'VAULT_ADDR': vault_url, 'VAULT_TOKEN': vault_token},
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if status.returncode == 0:
        # Vault is unsealed, check if secret path exists
        path_exists = subprocess.run(['vault', 'kv', 'get', '-format=json', secret_path], 
                                     env={'VAULT_ADDR': vault_url, 'VAULT_TOKEN': vault_token},
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if path_exists.returncode == 0:
            # Path exists, read and display output
            secret_value = path_exists.stdout.decode('utf-8').split('\n')[1]
            return f"Secret value for path {secret_path}: {secret_value}"
        else:
            # Path does not exist
            return f"Path {secret_path} does not exist"
    else:
        # Vault is sealed
        raise RuntimeError('Error checking Vault status')

=============================================================================

import subprocess

def check_vault(vault_url, vault_token, secret_path):
    # Check Vault status
    status = subprocess.run(['vault', 'status'], 
                            env={'VAULT_ADDR': vault_url, 'VAULT_TOKEN': vault_token},
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if status.returncode == 0:
        # Vault is unsealed, check if secret path exists
        path_exists = subprocess.run(['vault', 'kv', 'get', '-format=json', '-field=data', secret_path], 
                                     env={'VAULT_ADDR': vault_url, 'VAULT_TOKEN': vault_token},
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if path_exists.returncode == 0:
            # Path exists, read and display output
            secret_data = path_exists.stdout.decode('utf-8').strip()
            secret_dict = json.loads(secret_data)
            secret_key, secret_value = list(secret_dict.items())[0]
            return f"Secret key for path {secret_path}: {secret_key}, secret value: {secret_value}"
        else:
            # Path does not exist
            return f"Path {secret_path} does not exist"
    else:
        # Vault is sealed
        raise RuntimeError('Error checking Vault status')
        
================================================================================================    
    
import subprocess

def check_vault(vault_url, vault_token, secret_path):
    # Check Vault status
    status = subprocess.run(['vault', 'status'], 
                            env={'VAULT_ADDR': vault_url, 'VAULT_TOKEN': vault_token},
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if status.returncode == 0:
        # Vault is unsealed, list secrets in path
        path_list = subprocess.run(['vault', 'kv', 'list', secret_path], 
                                   env={'VAULT_ADDR': vault_url, 'VAULT_TOKEN': vault_token},
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if path_list.returncode == 0:
            # Path exists, read and display output
            output = path_list.stdout.decode('utf-8').strip()
            secrets = output.split('\n')
            secret_data = []
            for secret in secrets:
                if secret:
                    secret_get = subprocess.run(['vault', 'kv', 'get', secret_path + secret], 
                                                env={'VAULT_ADDR': vault_url, 'VAULT_TOKEN': vault_token},
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if secret_get.returncode == 0:
                        secret_data.append(secret_get.stdout.decode('utf-8').strip())
            
            return secret_data
        else:
            # Path does not exist
            return f"Path {secret_path} does not exist"
    else:
        # Vault is sealed
        raise RuntimeError('Error checking Vault status')

===============================================================================================================


import subprocess

def get_secrets(vault_url, vault_token, secrets_path):
    # Check if Vault is unsealed
    try:
        subprocess.check_output(['vault', 'status'],
                                env={'VAULT_ADDR': vault_url, 'VAULT_TOKEN': vault_token},
                                stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"Vault is sealed. Please unseal the vault: {e.output}")
        return None
    
    # Check if the specified secrets path exists and contains secrets (not directories)
    try:
        output = subprocess.check_output(['vault', 'kv', 'list', '-format', 'json', secrets_path],
                                          env={'VAULT_ADDR': vault_url, 'VAULT_TOKEN': vault_token},
                                          stderr=subprocess.STDOUT)
        secrets_list = output.decode('utf-8').strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving secrets list: {e.output}")
        return None
    
    # Check if the secrets path contains any directories (and exclude them from processing)
    secrets_list = [secret for secret in secrets_list if not secret.endswith('/')]
    
    # Retrieve the key-value pairs for each secret in the specified path
    secrets = []
    for secret in secrets_list:
        secret_path = f"{secrets_path}/{secret}"
        try:
            output = subprocess.check_output(['vault', 'kv', 'get', '-format', 'json', secret_path],
                                              env={'VAULT_ADDR': vault_url, 'VAULT_TOKEN': vault_token},
                                              stderr=subprocess.STDOUT)
            secret_data = output.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving secret data for {secret_path}: {e.output}")
            continue
        
        # Extract the key-value pairs from the JSON output
        try:
            secret_dict = {entry['key']: entry['value'] for entry in json.loads(secret_data)['data'].items()}
            secrets.append(secret_dict)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing secret data for {secret_path}: {e}")
            continue
    
    return secrets
