import os
from functions.check_seal import check_vault_seal_status
import hvac

# Read the URL and token from environment variables
url = os.environ['VAULT_URL']
token = os.environ['VAULT_TOKEN']

# Connect to Vault using the URL and token
client = hvac.Client(url=url, token=token)

# Call the check_vault_seal_status function from check_seal.py and pass in the client
is_sealed = check_vault_seal_status(client)

# Check the seal status
if is_sealed:
    print('Vault is sealed')
else:
    print('Vault is unsealed')
