from vault import connect_to_vault, get_paths_and_secrets, check_if_secret_exists

url = 'https://vault.example.com'
token = '<your-token>'
mount_point = 'TASK'
secret_path = 'hvac'

client = connect_to_vault(url, token)
paths, secrets = get_paths_and_secrets(client, mount_point)
print(f"Paths: {paths}")
print(f"Secrets: {secrets}")

if check_if_secret_exists(client, mount_point, secret_path):
    print(f"{secret_path} exists in {mount_point}")
else:
    print(f"{secret_path} does not exist in {mount_point}")
