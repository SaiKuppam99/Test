def check_and_write_secrets(client, mount_point, bin_dir):
    # Read paths from bin/paths.txt
    with open(f"{bin_dir}/paths.txt", "r") as f:
        paths = f.read().splitlines()

    # Loop through paths
    for path in paths:
        # Remove leading/trailing slashes
        path = path.strip("/")
        path_file_name = path.replace("/", "_")

        # Check if any secrets exist in path
        try:
            secrets = client.secrets.kv.v2.list_secrets(mount_point=mount_point, path=path)["data"]["keys"]
        except hvac.exceptions.InvalidPath:
            continue

        # Write secrets to file
        if secrets:
            with open(f"{bin_dir}/{path_file_name}_secret.txt", "w") as f:
                for secret in secrets:
                    data = client.secrets.kv.v2.read_secret_version(mount_point=mount_point, path=f"{path}/{secret}")["data"]["data"]
                    f.write(f"{secret}={data}\n")

        # Write path to file
        with open(f"{bin_dir}/{path_file_name}_path.txt", "w") as f:
            f.write(path)
