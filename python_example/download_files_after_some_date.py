import boto3
import os
import fnmatch
import datetime

from session_initiation import s3_cli

bucket_name = "YOUR_BUCKET_NAME"
s3_folder_path = "YOUR_S3_FOLDER_PATH"
local_download_path = "YOUR_LOCAL_DOWNLOAD_PATH"
pattern = "*.csv.gz"
date_threshold = datetime.datetime(2023, 7, 31)


def paginate_list_objects(s3_client, bucket_name, prefix):
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in page_iterator:
        for obj in page.get('Contents', []):
            yield obj


def download_matching_files():
    s3_client = s3_cli

    # Retrieve objects using pagination and filter based on the pattern and last modified date
    matching_files = [obj['Key'] for obj in paginate_list_objects(s3_client,
                                                                  bucket_name,
                                                                  s3_folder_path)
                      if fnmatch.fnmatch(obj['Key'],
                                         pattern)
                      and obj['LastModified'] > date_threshold]

    # Download the matching files to the local download path
    for file_key in matching_files:
        file_name = os.path.basename(file_key)
        local_file_path = os.path.join(local_download_path, file_name)
        s3_client.download_file(bucket_name, file_key, local_file_path)
        print(f"Downloaded: {file_key} => {local_file_path}")


if __name__ == "__main__":
    download_matching_files()
