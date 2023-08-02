# Manage Data in AWS S3 Bucket

## First things first

This repo aims at providing basic and specific commands or solutions so that anyone can better manage the data
stored on AWS S3 bucket.

Generally, for any kinds of data manipulation in local, it's better to download and configure the AWS CLI
before doing anything.

Download link: [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

After installation, remember to configure it by typing `aws configure` in your terminal. You will be asked to
input your AWS Access Key ID, AWS Secret Access Key, Default region name and Default output format. You can find these
information in your AWS account - My Security Credentials - Access keys (access key ID and secret access key), and for
Default region and Deafault output format, you can just leave it blank by pressing enter. Remember to generate your
own key first, and store it in a safe place.

Remember to test if everything is working by typing `aws s3 ls` in your terminal. If you don't see an error, then it's good to go.

Remember, when accessing the bucket that does not belong to you, very possibly you need to add `--request-payer` at
the end of every command. If not, you will get an error message saying that you don't have `permission` to access the bucket.

### (Optional - Only related to those having MFA enabled)

When MFA is enabled, and you have configured well on your local computer (by typing `aws configure` - the configuration
details will be saved to `~/.aws/credentials`), you can use the following command to initiate a session:

```angular2html
MFATOKEN=123456 MFAUSER=zhenning.li
AWSJSON=$(aws sts get-session-token --serial-number arn:aws:iam::731234585745:mfa/$MFAUSER --token-code $MFATOKEN);
export AWS_SESSION_TOKEN=$(echo $AWSJSON | jq -r .Credentials.SessionToken);
export AWS_SECRET_ACCESS_KEY=$(echo $AWSJSON | jq -r .Credentials.SecretAccessKey);
export AWS_ACCESS_KEY_ID=$(echo $AWSJSON | jq -r .Credentials.AccessKeyId)
```
Make sure to change `MFATOKEN`, `MFAUSER` and `--serial-number` value to your own MFA token, username and 
serial number. 

After pressing `Enter`, if there is no error then it's successfully connect.

### (Optional - Only related to those having multiple AWS accounts)

If you have multiple AWS accounts, and you want to iniate a session using one of your accounts, you have to add
`--profile my-second-account` at the end of the command. For example:

```angular2html
aws configure --profile victor-second-account
```
```angular2html
aws s3 ls --profile victor-second-account
```

## Basic commands

### List all buckets
```angular2html
aws s3 ls
```

### List all folders or files in a path
```angular2html
aws s3 ls s3://kaiko-internal-delivery-mit
```

If you want all files in all sub-folders to be listed, add `--recursive` at the end of the command.

### Copy a single file to local computer or to another bucket
To another bucket:
```angular2html
aws s3 cp "s3://bucket_name/kaiko-cohlcvvwap/gz_v1/1m_per_month/bw/btcusdt/bw_btcusdt_cohlcvvwap_1m_2019_08.csv.gz" "s3://my_own_buket/folder/"
```

To local computer:
```angular2html
```





## Special commands

### List all file names in a folder that are created of modified or updated after or before a certain date


###




# Other Reminders
1. It's better to always add `" "` to the path, especially when the path contains spaces (for example, Binance V2)
2. It's better to always add `--request-payer` at the end of the command, even for your own bucket, since it won't cost you anything.
3. It's always better to add `/` when executing any folder level commands like: `aws s3 ls s3://path/to/folder/`, because if you don't add `/`, it will
   just return you the name of this folder, and it's confusing indeed.
4. 
