import boto3
import pandas as pd
import tempfile

# Connect to the S3 service
s3 = boto3.client('s3')

# Download the XLS file to a temporary file
with tempfile.TemporaryFile() as tmp_file:
    s3.download_file('your-bucket-name', 'path/to/your-file.xls', tmp_file)

    # Rewind the file pointer to the beginning of the file
    tmp_file.seek(0)

    # Load the XLS file into a pandas DataFrame
    df = pd.read_excel(tmp_file)

# Convert the DataFrame to a JSON string
json_str = df.to_json(orient='records')

# Write the JSON string to a file
with open('path/to/output.json', 'w') as f:
    f.write(json_str)
