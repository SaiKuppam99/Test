#!/bin/bash

# Function to check if a command is available
is_command_available() {
    command -v "$1" >/dev/null 2>&1
}

# Check if saml2aws is installed
if ! is_command_available 'saml2aws'; then
    echo "saml2aws is not installed. Installing..."

    # Determine the system's platform (Linux or macOS)
    system_platform=$(uname -s | tr '[:upper:]' '[:lower:]')

    # Define the saml2aws download URL based on the platform
    download_url="https://github.com/Versent/saml2aws/releases/latest/download/saml2aws_${system_platform}_amd64"

    # Download saml2aws using curl
    sudo curl -Lo /usr/local/bin/saml2aws "$download_url"
    
    # Make saml2aws executable
    sudo chmod +x /usr/local/bin/saml2aws
fi

# Determine the AWS region to use
aws_region="${AWS_REGION:-eu-west-2}"

# Prompt for Azure AD username
read -p "Enter your Azure AD username (e.g., muzibsami02): " azure_ad_username

# Add the domain to the username
azure_ad_username_with_domain="${azure_ad_username}@gmail.co.uk"

# Continue with the rest of the script (configuration and authentication)
read -s -p "Enter your Azure AD password: " azure_ad_password
echo  # Print a new line after password input

read -p "Enter the Azure AD app ID: " azure_ad_app_id

# Configure saml2aws
saml2aws configure \
  --url 'https://account.activedirectory.windowsazure.com' \
  --username "$azure_ad_username_with_domain" \
  --idp-provider 'AzureAD' \
  --profile default \
  --region "$aws_region" \
  --app-id "$azure_ad_app_id" \
  --skip-prompt \
  --mfa 'Auto'

# Authenticate and obtain AWS credentials
saml2aws login
