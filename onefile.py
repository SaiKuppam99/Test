import hvac
import os


def check_secrets_and_write():
    # Initialize Vault client
    client = hvac.Client()

    # Check if Vault is already authenticated
    if not client.is_authenticated():
        # If not, authenticate using Vault Token
        vault_token = os.environ.get("VAULT_TOKEN")
        if not vault_token:
            raise Exception("VAULT_TOKEN environment variable not set")
        client.token = vault_token

    # Check if the secrets engine is mounted
    mount_path = "kv"
    mounts = client.sys.list_mounted_secrets_engines()
    if mount_path not in mounts:
        raise Exception(f"The '{mount_path}' secrets engine is not mounted")

    # Get a list of all secrets paths under the mount path
    secrets_paths = client.secrets.kv.v2.list_secrets(mount_path=mount_path)["data"]["keys"]
    secrets = {}
    paths = []

    # Iterate over the paths and retrieve the secrets
    for path in secrets_paths:
        # If the path ends with a '/', it is a subpath and should be added to the paths list
        if path.endswith("/"):
            paths.append(path)
        else:
            # Retrieve the secret and add it to the secrets dictionary
            secret = client.secrets.kv.v2.read_secret_version(mount_point=mount_path, path=path)["data"]["data"]
            secrets[path] = secret

    # Create the bin directory if it does not exist
    bin_dir = os.path.join(os.getcwd(), "bin")
    if not os.path.exists(bin_dir):
        os.mkdir(bin_dir)

    # Write the secrets and paths to separate files in the bin directory
    with open(os.path.join(bin_dir, "secrets.txt"), "w") as f:
        for key, value in secrets.items():
            f.write(f"{key}: {value}\n")

    with open(os.path.join(bin_dir, "paths.txt"), "w") as f:
        for path in paths:
            f.write(f"{path}\n")

    # Iterate over the paths and retrieve the secrets for sub-paths
    while paths:
        # Get the first path and remove it from the list of paths
        path = paths.pop(0)

        # Retrieve the secrets and sub-paths for the current path
        try:
            path_data = client.secrets.kv.v2.read_secret_version(mount_point=mount_path, path=path)["data"]["data"]
            if path_data:
                # Write the sub-paths to the paths file
                with open(os.path.join(bin_dir, "paths.txt"), "a") as f:
                    for key in path_data.keys():
                        sub_path = f"{path}/{key}"
                        f.write(f"{sub_path}\n")
                        paths.append(sub_path)

                # Write the secrets to a separate file
                with open(os.path.join(bin_dir, f"{path.replace('/', '_')}_secret.txt"), "w") as f:
                    for key, value in path_data.items():
                        f.write(f"{key}: {value}\n")
            else:
                print(f"No secrets found at path {path}")
        except Exception as e:
            print(f"Error reading secrets at path {path}: {e}")
