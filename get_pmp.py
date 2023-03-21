import requests
import json

def retrieve_credentials_from_pmp(api_token, pmp_server, password_id, output_file):
    api_url = f"https://{pmp_server}/restapi/1.5/passwords/{password_id}"

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(api_url, headers=headers, params={"format": "json"})

    password_details = response.json()

    with open(output_file, "w") as f:
        json.dump(password_details, f)

    return password_details

  api_token = "your-api-token"
pmp_server = "your-pmp-server"
password_id = "your-password-id"
output_file = "output-file-path.json"

password_details = retrieve_credentials_from_pmp(api_token, pmp_server, password_id, output_file)

print(password_details)
