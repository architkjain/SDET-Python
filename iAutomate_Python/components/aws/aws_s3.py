import boto3
import logging
from botocore.exceptions import ClientError
import os


class AWS_S3:

    def __init__(self):
        self.s3_client = boto3.client('s3')

    # Function to display all the buckets in AWS S3
    def display_buckets(self):
        try:
            s3 = boto3.resource('s3')
            for bucket in s3.buckets.all():
                logging.info(bucket.name)
                print(bucket.name)
        except ClientError as e:
            logging.error(e)

    # Function to create a bucket in default region (us-east-1)
    def create_bucket(self, bucket_name):
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    # Function to upload a file to existing bucket in default region (us-east-1)
    def s3_upload_file(self, file_path, bucket_name, object_name=None):
        """
        :param file_path: File path of the file to be uploaded.
        :param bucket_name: The name of the bucket to use.
        :param object_name:
        :return:
        """

        os.path.exists(file_path)
        if object_name is None:
            object_name = file_path
        try:
            self.s3_client.upload_file(file_path, bucket_name, object_name)
        except ClientError as e:
            logging.error(e)
            logging.error("Failed to upload the file")
            return False
        logging.info("File uploaded successfully")
        return True

    # Function to download a file to existing bucket in default region (us-east-1)
    def s3_download_file(self, file_path, bucket_name, object_name=None):
        """
        :param file_path: File path of the file to be uploaded.
        :param bucket_name: The name of the bucket to use.
        :param object_name:
        """
        if object_name is None:
            object_name = file_path
        try:
            self.s3_client.download_file(bucket_name, object_name, file_path)
        except ClientError as e:
            logging.error(e)
            logging.error("Failed to download the file")
            return False
        logging.info("File downloaded successfully")
        return True


if __name__ == "__main__":
    s3obj = AWS_S3()
    print("=======================================================")
    bucket_name = "archanab5"
    print(f"Creating a bucket:{bucket_name}")
    s3obj.create_bucket(bucket_name)
    print("=======================================================")
    print(f"Displaying all the buckets :")
    s3obj.display_buckets()
    print("========================================================")
    print("Uploading file to a bucket......")
    file_path = "D:\\log.txt"
    bucket_name = "archanab1"
    response = s3obj.s3_upload_file(file_path, bucket_name)
    if response:
        print(f"File {file_path} uploaded successfuly")
    else:
        print("Failed to upload the file")
    print("==========================================================")
    print("Downloading a file from a bucket......")
    response = s3obj.s3_download_file(file_path, bucket_name)
    if response:
        print(f"File {file_path} downloaded successfuly")
    else:
        print("Failed to download the file")
    print("==========================================================")
