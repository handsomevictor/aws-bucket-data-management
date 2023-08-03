import os
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from tqdm import tqdm
import shutil

from download_single_file import download_single_file_to_local


def download_files_from_s3_concurrent(all_files_to_download, max_workers=30, file_type='csv.gz',
                                      local_database_dir='data'):
    """
    Must run download_all_file_names first.
    Or you can also store the full path of all the files that you would like to download in a txt file or just memory,
    and pass it to this function.

    all_files_to_download: a list of full paths of files that you would like to download
    """

    print(f'Total number of files to download: {len(all_files_to_download)}')

    # download files
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        list(tqdm(pool.map(download_single_file_to_local,
                           all_files_to_download,
                           repeat(file_type)),
                  total=len(all_files_to_download)))
    print(f'All files are downloaded to {local_database_dir}!')


if __name__ == '__main__':
    ...
