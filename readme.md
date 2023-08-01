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


## (Optional - Only related to those having MFA enabled)



## Basic commands

### List all buckets
