from session_initiation import s3

source_bucket_name = "SOURCE_BUCKET_NAME"
destination_bucket_name = "DESTINATION_BUCKET_NAME"


def paginate_objects(s3_resource, bucket_name, prefix):
    bucket = s3_resource.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=prefix):
        yield obj


def synchronize_buckets():
    s3_resource = s3  # use boto3.resources instead of boto3.client

    # Paginate through objects in the source bucket
    for source_obj in paginate_objects(s3_resource, source_bucket_name, ''):
        source_key = source_obj.key
        destination_obj = s3_resource.Object(destination_bucket_name, source_key)

        if not destination_obj.exists() or source_obj.last_modified > destination_obj.last_modified:
            destination_obj.copy({'Bucket': source_bucket_name, 'Key': source_key})
            print(f"Synchronized: {source_key}")


if __name__ == "__main__":
    synchronize_buckets()
