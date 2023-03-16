import hvac
import os


def check_secrets(client, mount_path):
    # Check if the secrets engine is mounted
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

    # Write the secrets and paths to separate  files in the bin directory
    with open(os.path.join(bin_dir, "secrets.txt"), "w") as f:
        for key, value in secrets.items():
            f.write(f"{key}: {value}\n")

    with open(os.path.join(bin_dir, "paths.txt"), "w") as f:
        for path in paths:
            f.write(f"{path}\n")
