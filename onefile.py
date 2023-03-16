def create_folders_and_files(path):
    try:
        # Get the list of secrets and sub-paths for the current path
        path_list = client.secrets.kv.v2.list_secrets(mount_point=mount_point, path=path)["data"]["keys"]
        if path_list:
            for key in path_list:
                sub_path = f"{path}/{key}"
                full_path = os.path.join(bin_dir, sub_path)
                # Create a directory for the sub-path
                os.makedirs(full_path, exist_ok=True)
                # Recursively call the function if the sub-path has additional sub-paths or secrets
                create_folders_and_files(sub_path)

                # If the sub-path has secrets, create a file to store them
                try:
                    path_data = client.secrets.kv.v2.read_secret_version(mount_point=mount_point, path=sub_path)["data"]["data"]
                    if path_data:
                        with open(os.path.join(full_path, "secrets.txt"), "w") as f:
                            for key, value in path_data.items():
                                f.write(f"{key}: {value}\n")
                except Exception as e:
                    print(f"Error reading secrets at path {sub_path}: {e}")
        else:
            print(f"No secrets found at path {path}")
    except Exception as e:
        print(f"Error reading secrets at path {path}: {e}")
