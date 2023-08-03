from session_initiation import s3_cli

source_bucket_name = "SOURCE_BUCKET_NAME"
destination_bucket_name = "DESTINATION_BUCKET_NAME"


# Replace this list with the paths of the files you want to sync - Could be done by running the
# download_specific_file_names.py etc., just make sure there are full path names in the following list
file_path_mapping = {
    "path/to/source/file1.csv.gz": "destination/folder/file1.csv.gz",
    "path/to/source/file2.csv.gz": "destination/folder/file2.csv.gz",
    # Add more mappings as needed
}


def synchronize_buckets():
    # Create Boto3 S3 client
    s3_client = s3_cli

    for source_file_path, destination_file_path in file_path_mapping.items():

        # Copy the file from the source bucket to the destination bucket with the specified key
        copy_source = {'Bucket': source_bucket_name, 'Key': source_file_path}
        s3_client.copy_object(Bucket=destination_bucket_name, CopySource=copy_source, Key=destination_file_path)
        print(f"Synchronized: {source_file_path} => {destination_file_path}")


if __name__ == "__main__":
    synchronize_buckets()
