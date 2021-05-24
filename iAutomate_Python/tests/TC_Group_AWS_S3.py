# Author: Vikram
import os
import time
import logging
from datetime import datetime
from framework import Status
from framework import AutoTest
from framework.annotations import groupInit, groupCleanup
from components.aws.aws_s3 import AWS_S3


@groupInit
def init():
    print('Inside groupInit()')


class TestCase_create_s3_bucket(AutoTest):
    """ Testcase to test creation of S3 bucket.
        Upload the file to bucket
        Download the uploaded file
    """

    def set_up(self):
        self.aws = AWS_S3()
        # Define bucket name
        self.bucket_name = "testbucket" + datetime.now().strftime("%d%m%Y%H%M%S")
        print(f"Bucket Name is{self.bucket_name}")
        self.file_name = os.getcwd() + "\\" + "test_file.txt"
        if not os.path.isfile(self.file_name):
            with open(self.file_name, 'w') as fh:
                fh.write("This is a test file")

    def test(self):
        print("Creating a bucket:{}".format(self.bucket_name))
        logging.info("Creating a bucket:{}".format(self.bucket_name))
        if self.aws.create_bucket(self.bucket_name):
            self.log_step_result('Step 1', 'Create Bucket',
                                 'Verify : Creation of bucket should be successful',
                                 'Successful', Status.PASS)

            # Upload file to S3 bucket
            if self.aws.s3_upload_file(self.file_name, self.bucket_name):
                self.log_step_result('Step 2', 'Upload file to bucket',
                                     'Verify : File upload should be successful',
                                     'Successful', Status.PASS)
                os.remove(self.file_name)
            else:
                self.log_step_result('Step 2', 'Upload file to bucket',
                                     'Verify : File upload should be successful',
                                     'Failed to upload file', Status.FAIL)

            # Download file from S3 bucket
            if self.aws.s3_download_file(self.file_name, self.bucket_name):
                self.log_step_result('Step 3', 'Download file to bucket',
                                     'Verify : Download of file should be successful',
                                     'Successful', Status.PASS)
            else:
                self.log_step_result('Step 3', 'Download file to bucket',
                                     'Verify : Download of file should be successful',
                                     'Failed to download file', Status.FAIL)
        else:
            self.log_step_result('Step 1', 'Create Bucket',
                                 'Verify : Creation of bucket should be successful',
                                 'Failed to create bucket', Status.FAIL)

    def tear_down(self):
        try:
            os.remove(self.file_name)
        except FileNotFoundError:
            logging.info("File does not exist")


class TestCase_create_and_dislpay_s3_bucket(AutoTest):
    """ Test test """

    def set_up(self):
        self.aws = AWS_S3()
        # Define bucket name
        self.bucket_name = "testbucket" + datetime.now().strftime("%d%m%Y%H%M%S")

    def test(self):
        print("Creating a bucket:{}".format(self.bucket_name))
        logging.info("Creating a bucket:{}".format(self.bucket_name))
        if self.aws.create_bucket(self.bucket_name):
            self.log_step_result('Step 1', 'Create Bucket',
                                 'Verify : Creation of bucket should be successful',
                                 'Successful', Status.PASS)
        else:
            self.log_step_result('Step 1', 'Create Bucket',
                                 'Verify : Creation of bucket should be successful',
                                 'Failed to create bucket', Status.FAIL)

        if self.aws.display_buckets():
            self.log_step_result('Step 2', 'Display Bucket',
                                 'Verify : List of all bucket should be displayed',
                                 'Successful', Status.PASS)
        else:
            self.log_step_result('Step 2', 'Display Bucket',
                                 'Verify : List of all bucket should be displayed',
                                 'Failed to list buckets', Status.FAIL)

    def tear_down(self):
        pass


@groupCleanup
def clean():
    print('Inside groupCleanup()')
