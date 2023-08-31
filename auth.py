import subprocess
import sys
import platform
import os

# Function to check if a command is available
def is_command_available(command):
    try:
        subprocess.check_output([command, '--version'])
        return True
    except subprocess.CalledProcessError:
        return False

# Check if saml2aws is installed
if not is_command_available('saml2aws'):
    print("saml2aws is not installed. Installing...")

    try:
        # Determine the system's platform (Linux or macOS)
        system_platform = platform.system().lower()

        # Define the saml2aws download URL based on the platform
        download_url = f'https://github.com/Versent/saml2aws/releases/latest/download/saml2aws_{system_platform}_amd64'

        # Download saml2aws using curl
        download_command = [
            'curl',
            '-Lo', '/usr/local/bin/saml2aws',
            download_url
        ]
        subprocess.run(download_command, check=True)

        # Make saml2aws executable
        os.chmod('/usr/local/bin/saml2aws', 0o755)

    except subprocess.CalledProcessError:
        print("Failed to automatically install saml2aws.")
        sys.exit(1)

# Determine the AWS region to use
aws_region = os.environ.get('AWS_REGION', 'eu-west-2')

# Continue with the rest of the script (configuration and authentication)
azure_ad_username = input("Enter your Azure AD username: ")
azure_ad_password = input("Enter your Azure AD password: ")
azure_ad_app_id = input("Enter the Azure AD app ID: ")

# ... (rest of the configuration and authentication steps)
