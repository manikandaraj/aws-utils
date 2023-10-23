"""
@Author = Manikandaraj Srinivasan
@Date = 2023-10-23
@Description = This script is used to create S3 bucket and apply tags to it.
@Website = https://www.manikandaraj.com
"""

import argparse
from com.utils.aws_args_validator import AWSArgsValidator
from com.utils.s3_service import S3Service

def create_and_configure_s3_bucket(aws_region, bucket_name, tags):
    try:
        s3_service = S3Service(aws_region)
        if not s3_service.check_if_bucket_exists(bucket_name):
            print(f"Bucket doesn't exists - :{bucket_name}")
            s3_service.create_s3_bucket(bucket_name)

        s3_service.apply_tags(bucket_name, tags)
        s3_service.block_all_public_access(bucket_name)
        s3_service.disable_static_website_hosting(bucket_name)
        s3_service.update_bucket_encryption(bucket_name)
        s3_service.update_bucket_ownership_control(bucket_name)
    except Exception as exc_obj:
        print(f"Exception in creating S3 Bucket: {exc_obj}")

def main():
    parser = argparse.ArgumentParser(description="AWS S3 Utility")
    parser.add_argument(
        "--aws-region",
        required=True,
        type=AWSArgsValidator.validate_aws_region,
        help="AWS Region"
    )
    parser.add_argument(
        "--bucket-name",
        required=True,
        type=AWSArgsValidator.validate_bucket_name,
        help="S3 Bucket Name"
    )
    parser.add_argument(
        "--tags",
        nargs='+',
        type=AWSArgsValidator.validate_tags,
        help="Tags to apply",
        default=[]
    )
    args = parser.parse_args()

    print(f"AWS Region: {args.aws_region}")
    print(f"Bucket Name: {args.bucket_name}")
    print(f"Tags: {args.tags}")
    create_and_configure_s3_bucket(args.aws_region, args.bucket_name, args.tags)

if __name__ == "__main__":
    main()
