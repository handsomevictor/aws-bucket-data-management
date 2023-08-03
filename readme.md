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

If you have multiple AWS accounts, and you want to initiate a session using one of your accounts, you have to add
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

### Copy a single file to local computer or to another bucket - use cp command
To another bucket:
```angular2html
aws s3 cp "s3://bucket_name/kaiko-cohlcvvwap/gz_v1/bw_btcusdt_cohlcvvwap_1m_2019_08.csv.gz" "s3://my_own_buket/folder/"
```

To local computer:
```angular2html
aws s3 cp "s3://bucket_name/kaiko-cohlcvvwap/gz_v1/bw_btcusdt_cohlcvvwap_1m_2019_08.csv.gz" "/local/path"
```

### Copy all files in a folder to local computer or to another bucket - use sync or cp command
Both sync and cp command will work for this purpose. The difference is that sync command will only copy the files that
are not existing in the destination folder, while cp command will copy all files in the source folder to the destination
folder, even if they are already existing in the destination folder.

In summary, if you want to copy the entire contents of a folder from an S3 bucket to your local 
machine, you can use cp with `--recursive`. However, if you want to synchronize the contents 
between the S3 bucket and your local machine, updating only the necessary files, you should use 
sync.

```angular2html
aws s3 sync s3://bucket_name/specific/path/if/needed/ /path/to/bucket/or/local/ --exclude "*" --include "*.csv.gz"
```

```angular2html
aws s3 cp s3://bucket_name/specific/path/if/needed/ /path/to/bucket/or/local/ --recursive --exclude "*" --include "*.csv.gz"
```

Explanation of `--exclude` and `--include`: 

`--exclude` and `--include` are used to specify which files (it's a [wildcard pattern matching](https://www.geeksforgeeks.org/wildcard-pattern-matching/)
mechanism) to copy. 

For example, if you want to copy all files except those with `.csv.gz`, you can use `--exclude "*.csv.gz"`.

But when you only want to just download those files with `.csv.gz` extension, you have to use `--exclude "*"` and 
`--include "*.csv.gz"` -> it means, exclude everything, then only select those that satisfy the `--include` pattern. 

### Remove a single file or a folder

To remove a folder, remember to add `--recursive`:
```angular2html
aws s3 rm s3://bucket_name/specific/path/if/needed/ --recursive
```

To remove a single file, just rm + the path to the file.

Remove files that satisfy some special pattern in the file name (same wildcard matching mechanism):
```angular2html
aws s3 rm s3://bucket_name/specific/path/if/needed/ --recursive --exclude "*" --include "*.csv.gz"
```


### Create a downloadable link for others to download anything in your bucket
Reminder: this only works for single file, not for a folder. You have to compressed the folder before using this command.
```angular2html
aws s3 presign s3://bucket_name/file_name --expires-in 604800
```

604800 unit is in second, and it's 7 days. It's the longest time you can set for the link to be valid.



## Special Commands

### Only download the data that is between 2017 Jan to 2020 April for certain exchanges

```angular2html
aws s3 sync s3://bucket_name/kaiko-trades/gz_v1/ /path/to/your/folder --exclude "*" --include "2017_*/*/*" --include "2018_*/*/*" --include "2019_*/*/*" --include "2020_0[1-4]/*/*" --exclude "*/*/*/*" --include "*Binance V2*" --include "*BinanceUS*" --include "*Bitfinex*" --include "*BitMEX*" --include "*Bitstamp*" --include "*Coinbase*" --include "*Gemini*" --include "*Huobi*" --include "*Kraken*" --include "*OkCoin*"
```

The following one will download corresponding data for all exchanges:
```angular2htmls
aws s3 sync s3://kaiko-internal-delivery-syracuse/kaiko-trades/gz_v1/ /path/to/your/folder --exclude "*" --include "2017_*/*/*" --include "2018_*/*/*" --include "2019_*/*/*" --include "2020_0[1-4]/*/*"
```


### List all file names in a folder that are created of modified or updated after or before a certain date

- In AWS CLI, you can use the following command to satisfy this need:

   ```angular2html
   aws s3 ls "s3://bucket_name/kaiko-trades/Binance V2/BTCUSDT/2023_07/" --recursive --human-readable --summarize | awk '$1 > "2023-07-25" || ($1 == "2023-07-25" && $2 >= "07:00") {print $0}'
   ```
   If you want to download this list, you can add `>> /path/to/your/file.txt` at the end of the command to save the result to a local txt file.

- In Python, please refer to this file.......
    
    

### Only download files that are created or modified after or before a certain date


### 


## Special Needs

### Python Related

- **Download single file to local computer**

    Code can be found [here](./python_example/download_single_file.py)
    
    More specifically, the download function is the following one:
    ```python
    s3_cli.download_file(Bucket=bucket_name,
                         Key=file_name,  # file_name is the full path to the file in the bucket
                         Filename=local_file_name)  # local_file_name is the full path you want the local file to have in your computer
    ```

- **Download the list of names of all files for convenience of downloading filtered files to local**
    
    Code can be found [here](./python_example/download_all_file_names.py)
    
    More specifically, the download function is the following one:
    ```python
    kwargs = {'Bucket': bucket_name, 'Prefix': folder_name}
    s3_cli.list_objects_v2(**kwargs)
    ```

- **Download many files parallelly**
    
    Code can be found [here](./python_example/download_concurrent.py)
    
    More specifically, the download function contains multiprocessing or multithreading skills in Python:
    ```python
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        list(tqdm(pool.map(download_single_file_to_local,
                           all_files_to_download,
                           repeat(file_type)),
                  total=len(all_files_to_download)))
    ```
    Basically, put the full paths of files that you would like to download as a list and pass it to
    `all_files_to_download`, then the multiprocessing or multithreading will execute the download single file function
    in a parallel way for the list of files.



- **Download files that are created or modified after or before a certain date**
    Code can be found [here](./python_example/download_concurrent.py)


#### Automation of downloading / transferring the newly created / updated files to local or another bucket
First method: use `aws s3 sync` command with `--exclude "*" --include "*.csv.gz"` to download all files with `.csv.gz` extension
that are not existing in the destination folder.






# Other Reminders
1. It's better to always add `" "` to the path, especially when the path contains spaces (for example, Binance V2)
2. It's better to always add `--request-payer` at the end of the command, even for your own bucket, since it won't cost you anything.
3. It's always better to add `/` when executing any folder level commands like: `aws s3 ls s3://path/to/folder/`, because if you don't add `/`, it will
   just return you the name of this folder, and it's confusing indeed.
4. More wildcard pattern matching examples can be found [here](https://www.geeksforgeeks.org/wildcard-pattern-matching/).
5. 
