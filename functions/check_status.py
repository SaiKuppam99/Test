def check_vault_seal_status(client):
    seal_status = client.sys.read_seal_status()
    return seal_status['sealed']
