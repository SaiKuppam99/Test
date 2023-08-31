#!/bin/bash

# Function to check if a command is available
is_command_available() {
    command -v "$1" >/dev/null 2>&1
}

# Check if saml2aws is already installed
if is_command_available 'saml2aws'; then
    echo "saml2aws is already installed."
else
    # Create the directory for saml2aws if it doesn't exist
    mkdir -p ~/.local/bin

    echo "saml2aws is not installed. Installing..."

    # Get the latest release version from GitHub
    CURRENT_VERSION=$(curl -Ls https://api.github.com/repos/Versent/saml2aws/releases/latest | grep 'tag_name' | cut -d'v' -f2 | cut -d'"' -f1)

    # Download and extract saml2aws
    wget -c "https://github.com/Versent/saml2aws/releases/download/v${CURRENT_VERSION}/saml2aws_${CURRENT_VERSION}_linux_amd64.tar.gz" -O - | tar -xzv -C ~/.local/bin

    # Make saml2aws executable
    chmod u+x ~/.local/bin/saml2aws

    # Update the command hash
    hash -r

    echo "saml2aws has been installed."
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
