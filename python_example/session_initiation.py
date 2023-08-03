import boto3

session = boto3.Session()
s3 = boto3.resource('s3',
                    aws_secret_access_key="Your secret key",
                    aws_access_key_id="Your access key"
                    )
s3_cli = boto3.client('s3',
                      aws_secret_access_key="Your secret key",
                      aws_access_key_id="Your access key"
                      )

# Now the session is initiated, you can use the s3 and s3_cli objects to interact with S3 like downloading/uploading
# files, getting the list of files that are in a bucket, etc.

# This is not working for MFA, for MFA enabled initiation, there will be a separate script soon to be uploaded

