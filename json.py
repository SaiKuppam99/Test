import os
import boto3
import pandas as pd
import tempfile

def xls_to_json(bucket_name, file_path, columns):
    # Set the AWS profile
    os.environ['AWS_PROFILE'] = 'my-profile'

    # Connect to the S3 service
    s3 = boto3.client('s3')

    # Download the XLS file to a temporary file
    with tempfile.TemporaryFile() as tmp_file:
        s3.download_file(bucket_name, file_path, tmp_file)

        # Rewind the file pointer to the beginning of the file
        tmp_file.seek(0)

        # Load only the selected columns into a pandas DataFrame
        df = pd.read_excel(tmp_file, usecols=columns)

    # Check for empty values in the User Account and Password columns
    mask = df[['User Account', 'Password']].isnull().any(axis=1)
    if mask.any():
        # Empty values found
        print('Empty values found in the User Account or Password columns:')
        print(df[mask])
    else:
        # No empty values found
        print('No empty values found in the User Account or Password columns')

    # Convert the DataFrame to a JSON string
    json_str = df.to_json(orient='records')
    
    return json_str
