"""
@Author = Manikandaraj Srinivasan
@Date = 2023-10-23
@Description = This module contains S3 functions.
@Website = https://www.manikandaraj.com
"""

import botocore
import boto3

class S3Service:
    def __init__(self, aws_region):
        self.aws_region = aws_region
        self.s3_client = boto3.client('s3', region_name=aws_region)
        print(f"Initialized S3Service with AWS region: {aws_region}")

    """
    Check if the specified S3 bucket exists.
    """
    def check_if_bucket_exists(self, bucket_name):
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} exists.")
            return True
        except Exception as e:
            print(f"Bucket {bucket_name} does not exist. {e}")
            return False

    """
    Create a new S3 bucket with specified options.
    """
    def create_s3_bucket(self, bucket_name):
        try:
            response = self.s3_client.create_bucket(
                Bucket=bucket_name,
                ObjectOwnership='BucketOwnerEnforced',
                ObjectLockEnabledForBucket=False,
                ACL='private'
            )
            if(response.get("Location", "") == f"/{bucket_name}"):
                bucket_created = True
                print(f"Bucket {bucket_name} created successfully.")
        except Exception as e:
            print(f"Failed to create bucket {bucket_name}. {e}")

    """
    Apply tags to the specified S3 bucket.
    """
    def apply_tags(self, bucket_name, resource_tags):
        try:
            self.s3_client.put_bucket_tagging(
                Bucket=bucket_name,
                Tagging={'TagSet': [{'Key': tag.split('=')[0], 'Value': tag.split('=')[1]} for tag in resource_tags]}
            )
            print(f"Tags applied to bucket {bucket_name}.")
        except Exception as e:
            print(f"Failed to apply tags to bucket {bucket_name}. {e}")

    """
    Block all public access to the specified S3 bucket.
    """
    def block_all_public_access(self, bucket_name):
        try:
            self.s3_client.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
            print(f"Blocked all public access to bucket {bucket_name}.")
        except Exception as e:
            print(f"Failed to block public access to bucket {bucket_name}. {e}")

    def disable_bucket_versioning(self):
        try:
            self.s3_client.put_bucket_versioning(Bucket=self.bucket_name, VersioningConfiguration={'Status': 'Suspended'})
            return True
        except botocore.exceptions.ClientError as exc_obj:
            print(f"Exception in Disabling Bucket Versioning: {exc_obj}")
        return False
    """
    Disable static website hosting for the specified S3 bucket.
    """
    def disable_static_website_hosting(self, bucket_name):
        try:
            self.s3_client.delete_bucket_website(Bucket=bucket_name)
            return True
        except botocore.exceptions.ClientError as exc_obj:
            print(f"Exception in Disabling Static Website Hosting: {exc_obj}")
        return False

    """
    Update bucket encryption settings.
    """
    def update_bucket_encryption(self, bucket_name):
        try:
            self.s3_client.put_bucket_encryption(
                Bucket = bucket_name,
                ServerSideEncryptionConfiguration={
                    'Rules': [
                        {
                            'ApplyServerSideEncryptionByDefault': {
                                'SSEAlgorithm': 'AES256'
                            },
                            'BucketKeyEnabled': True
                        }
                    ]
                }
            )
            print(f"Bucket encryption updated for bucket {bucket_name}.")
        except Exception as e:
            print(f"Failed to update bucket encryption for bucket {bucket_name}. {e}")

    """
    Update bucket ownership control settings.
    """
    def update_bucket_ownership_control(self, bucket_name):
        try:
            self.s3_client.put_bucket_ownership_controls(
                Bucket=bucket_name,
                OwnershipControls={
                    'Rules': [
                        {
                            'ObjectOwnership': 'BucketOwnerEnforced'
                        }
                    ]
                }
            )
            print(f"Bucket ownership control updated for bucket {bucket_name}.")
        except Exception as e:
            print(f"Failed to update bucket ownership control for bucket {bucket_name}. {e}")

