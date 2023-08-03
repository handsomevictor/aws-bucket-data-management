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

# The following is the initiated session working for MFA enabled accounts, it is commented out

# session = boto3.Session()
#
# mfa_serial = session._session.full_config['profiles']['default']['mfa_serial']
# # if you have multiple profiles, you should specify the profile name here by changing the 'default' to the profile name
#
# mfa_token = input('Please enter your 6 digit MFA code:')
# sts = session.client('sts')
# MFA_validated_token = sts.get_session_token(SerialNumber=mfa_serial, TokenCode=mfa_token)
#
# print(MFA_validated_token)
# print(mfa_serial)
#
# s3 = boto3.resource('s3',
#                     aws_session_token=MFA_validated_token['Credentials']['SessionToken'],
#                     aws_secret_access_key=MFA_validated_token['Credentials']['SecretAccessKey'],
#                     aws_access_key_id=MFA_validated_token['Credentials']['AccessKeyId']
#                     )
# s3_cli = boto3.client('s3',
#                       aws_session_token=MFA_validated_token['Credentials']['SessionToken'],
#                       aws_secret_access_key=MFA_validated_token['Credentials']['SecretAccessKey'],
#                       aws_access_key_id=MFA_validated_token['Credentials']['AccessKeyId']
#                       )
