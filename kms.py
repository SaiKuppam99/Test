import boto3

def list_kms_keys(region):
    kms_client = boto3.client('kms', region_name=region)

    response = kms_client.list_keys()
    keys = response.get('Keys', [])

    return keys

def check_rotation_status(region, key_id):
    kms_client = boto3.client('kms', region_name=region)

    response = kms_client.get_key_rotation_status(KeyId=key_id)
    rotation_enabled = response['KeyRotationEnabled']

    return rotation_enabled

def enable_key_rotation(region, key_id):
    kms_client = boto3.client('kms', region_name=region)

    try:
        kms_client.enable_key_rotation(KeyId=key_id)
        print(f"Enabled key rotation for {key_id} in {region}")
    except Exception as e:
        print(f"Error enabling key rotation for {key_id} in {region}: {e}")

def main():
    # Replace these values with your AWS account ID and region
    aws_accounts = ['account_id_1', 'account_id_2']
    regions = ['us-east-1', 'us-west-2']

    for account_id in aws_accounts:
        for region in regions:
            print(f"Checking KMS keys in {region} for account {account_id}")

            keys = list_kms_keys(region)

            for key in keys:
                key_id = key['KeyId']
                rotation_enabled = check_rotation_status(region, key_id)

                if not rotation_enabled:
                    enable_key_rotation(region, key_id)
                else:
                    print(f"Key rotation is already enabled for {key_id} in {region}")

if __name__ == "__main__":
    main()
