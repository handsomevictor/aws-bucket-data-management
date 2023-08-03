import os
import boto3
import gzip

from session_initiation import s3_cli


def download_single_file_to_local(single_file_s3_dir, local_database_dir, bucket_name, file_type=None):
    """
    Download a single file from S3 to local
    :param single_file_s3_dir:
    :param local_database_dir: should be a folder name, not a file name
    :param bucket_name:
    :param file_type: if filled with 'csv.gz', the file will be unzipped after downloading, if not then do nothing
    :return:
    """
    file_name = single_file_s3_dir

    download_target_dir = os.path.join(os.getcwd(), local_database_dir)
    download_target_file_dir = os.path.join(download_target_dir, file_name)

    try:
        if not os.path.exists(download_target_dir):
            os.makedirs(download_target_dir)
    except FileExistsError:
        pass

    temp_dir = '/'.join(download_target_file_dir.split('/')[:-1])  # get the file dir for creating folders locally

    try:
        if not os.path.exists(os.path.join(os.getcwd(), local_database_dir, temp_dir)):
            os.makedirs(temp_dir)
    except FileExistsError:
        pass

    s3_cli.download_file(Bucket=bucket_name,
                         Key=file_name,
                         Filename=os.path.join(os.getcwd(),
                                               local_database_dir,
                                               download_target_file_dir))

    # Now unzip the file from gz to csv if necessary
    if file_type == 'csv.gz':
        file_name_unzipped = os.path.join(os.getcwd(), local_database_dir,
                                          file_name.split('/')[-1].split('.')[0] + '.csv')
        with gzip.open(download_target_file_dir, 'rb') as f_in:
            with open(file_name_unzipped, 'wb') as f_out:
                f_out.writelines(f_in)
        os.remove(download_target_file_dir)


if __name__ == '__main__':
    ...
