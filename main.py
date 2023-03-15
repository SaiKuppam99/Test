from functions.check_seal import check_vault_seal_status
import hvac

# Define the URL and token variables
url = 'https://vault.example.com'
token = '<your-token>'

# Connect to Vault using the URL and token
client = hvac.Client(url=url, token=token)

# Call the check_vault_seal_status function from check_seal.py and pass in the client
is_sealed = check_vault_seal_status(client)

# Check the seal status
if is_sealed:
    print('Vault is sealed')
else:
    print('Vault is unsealed')
