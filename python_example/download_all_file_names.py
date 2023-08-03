import os
import boto3
import gzip

from session_initiation import s3_cli


def download_all_file_names_in_folder(bucket_name, folder_name):
    """
    Because s3_cli.list_objects_v2 only returns 1000 files at a time, we need to use a while loop to get all files
    """

    file_names = []
    continuation_token = None
    i = 0
    while True:
        kwargs = {'Bucket': bucket_name, 'Prefix': folder_name}

        if continuation_token:
            kwargs['ContinuationToken'] = continuation_token

        response = s3_cli.list_objects_v2(**kwargs)
        file_names.extend([item['Key'] for item in response.get('Contents', [])])
        if not response.get('IsTruncated'):
            break
        continuation_token = response.get('NextContinuationToken')
        i += 1
        print(f'Iteration {i}')

    # save file names
    all_names_dir = os.path.join(os.getcwd(), f'all_files_dir_aws_in_subfolder_{folder_name.split("/")[0]}.txt')
    with open(all_names_dir, 'w') as f:
        for file in file_names:
            f.write(file + '\n')


if __name__ == '__main__':
    ...
