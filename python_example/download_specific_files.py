"""
This script is not using concurrency and is downloading files one at a time.
"""

import boto3
import os
import fnmatch

from session_initiation import s3_cli

# Replace these values with your AWS credentials and S3 bucket information
aws_access_key_id = "YOUR_ACCESS_KEY"
aws_secret_access_key = "YOUR_SECRET_ACCESS_KEY"
bucket_name = "YOUR_BUCKET_NAME"
s3_folder_path = "YOUR_S3_FOLDER_PATH"
local_download_path = "YOUR_LOCAL_DOWNLOAD_PATH"
pattern = "*.csv.gz"


def paginate_list_objects(s3_client, bucket_name, prefix):
    """
    This function uses the boto3 client to paginate through the list of objects in the specified S3 bucket and prefix.
    Aim to process the objects in the bucket in batches of 1000, so it can let you know it's still working when there
    are a lot of files to process.
    """
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in page_iterator:
        for obj in page.get('Contents', []):
            yield obj['Key']


def download_matching_files():
    s3_client = s3_cli

    # Retrieve objects using pagination and filter based on the pattern using Python's fnmatch module
    matching_files = [obj_key for obj_key in paginate_list_objects(s3_client,
                                                                   bucket_name,
                                                                   s3_folder_path)
                      if fnmatch.fnmatch(obj_key,
                                         pattern)]

    # Download the matching files to the local download path
    for file_key in matching_files:
        file_name = os.path.basename(file_key)
        local_file_path = os.path.join(local_download_path, file_name)
        s3_client.download_file(bucket_name, file_key, local_file_path)
        print(f"Downloaded: {file_key} => {local_file_path}")


if __name__ == "__main__":
    download_matching_files()
