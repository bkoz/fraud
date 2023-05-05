#
# Simple boto3 client to upload a file to S3 compatible object store.
#

import boto3
import os

def upload_file(s3_client, file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    :param s3_client: The client connection handle.
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If the S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":

    #
    # Connect to S3. Make sure the environment variables listed
    # below are set.
    #
    client = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        endpoint_url=os.getenv("AWS_S3_ENDPOINT")
    )

    print("List buckets:")
    print(client.list_buckets())
    print()

    print("Uploading file to S3...")

    upload_file(client, "s3test.py", "TAMU-Vault1")

