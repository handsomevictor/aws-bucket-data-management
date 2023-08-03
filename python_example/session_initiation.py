import os
import boto3
import gzip
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from tqdm import tqdm
import shutil

session = boto3.Session()
s3 = boto3.resource('s3',
                    aws_secret_access_key=session.get_credentials().get_frozen_credentials().secret_key,
                    aws_access_key_id=session.get_credentials().get_frozen_credentials().access_key
                    )
s3_cli = boto3.client('s3',
                      aws_secret_access_key=session.get_credentials().get_frozen_credentials().secret_key,
                      aws_access_key_id=session.get_credentials().get_frozen_credentials().access_key
                      )

# Now the session is initiated, you can use the s3 and s3_cli objects to interact with S3 like downloading/uploading
# files, getting the list of files that are in a bucket, etc.
