import boto3
import json

def create_secrets_from_file(file_path, cluster_identifier, kms_key_id, profile_name, tags=None):
    """
    Create secrets in AWS Secrets Manager based on a JSON file.

    :param file_path: The path to the JSON file containing the secrets.
    :param cluster_identifier: The identifier of the RDS cluster associated with the secrets.
    :param kms_key_id: The ARN or alias of the KMS key to use for encrypting the secrets.
    :param profile_name: The name of the AWS profile to use for authentication.
    :param tags: A list of tags to apply to the secrets (optional).
    """
    # Read the JSON file
    with open(file_path) as f:
        secrets = json.load(f)

    # Set the cluster and host variables
    host = f"{cluster_identifier}.cluster-123456789012.us-east-1.rds.amazonaws.com"

    # Create a Secrets Manager client using the specified AWS profile
    session = boto3.Session(profile_name=profile_name)
    client = session.client('secretsmanager')

    # Loop through the secrets and create them in Secrets Manager
    for secret in secrets:
        name = f"myapp-{secret['User Account']}"  # Use a custom naming convention
        response = client.create_secret(
            Name=name,
            SecretString=json.dumps({
                'SecretType': 'db',
                'dbClusterIdentifier': cluster_identifier,
                'engine': 'mysql',
                'host': host,
                'password': secret['Password'],
                'port': '3306',
                'username': secret['User Account'],
                # Add more variables here as needed
            }),
            Description=f"Secret for {name} database access",
            Tags=tags,
            KmsKeyId=kms_key_id,
            RecoveryWindowInDays=7,
            AutoRotateAfterDays=30,
        )
        print(f"Created secret {response['ARN']} with name {name}")
