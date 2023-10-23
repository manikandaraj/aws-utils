"""
@Author = Manikandaraj Srinivasan
@Date = 2023-10-23
@Description = This module contains functions for validating AWS CLI arguments.
@Website = https://www.manikandaraj.com
"""

import re
import argparse

class AWSArgsValidator:
    @staticmethod
    def validate_aws_region(value):
        valid_regions = [
            'us-east-1',  'us-east-2',  'us-west-1',  'us-west-2',
            'ap-southeast-1',  'ap-southeast-2',  'ap-southeast-3',  'ap-southeast-4',
            'ap-northeast-1',  'ap-northeast-2',  'ap-northeast-3',
            'ap-south-1',  'ap-south-2', 
            'eu-west-1',  'eu-west-2',  'eu-west-3',
            'eu-north-1',  'eu-south-1',  'eu-south-2',  'eu-central-1',  'eu-central-2',
            'sa-east-1',  'ap-east-1',  'me-south-1',  'me-central-1',
            'il-central-1',  'af-south-1',  'ca-central-1'
        ]
        if value not in valid_regions:
            raise argparse.ArgumentTypeError(f"Invalid AWS region. Allowed values are {', '.join(valid_regions)}")
        return value

    @staticmethod
    def validate_bucket_name(value):
        return value
        if not (3 <= len(value) <= 63):
            raise argparse.ArgumentTypeError("Bucket name must be between 3 and 63 characters long.")
        
        if not re.match("^[a-z0-9.-]*$", value):
            raise argparse.ArgumentTypeError("Bucket name can consist only of lowercase letters, numbers, dots (.), and hyphens (-).")
        
        if not re.match("^[a-z0-9]", value) or not re.match("[a-z0-9]$", value):
            raise argparse.ArgumentTypeError("Bucket name must begin and end with a letter or number.")
        
        if ".." in value:
            raise argparse.ArgumentTypeError("Bucket name must not contain two adjacent periods.")
        
        if re.match(r"^\d+\.\d+\.\d+\.\d+$", value):
            raise argparse.ArgumentTypeError("Bucket name must not be formatted as an IP address.")
        
        return value

    @staticmethod
    def validate_tags(tag):
        try:
            tag_name, tag_value = tag.split('=')
        except ValueError:
            raise argparse.ArgumentTypeError("Tags should be in the format TAG_NAME=TAG_VALUE.")
        
        if not re.match("^[a-zA-Z_]+$", tag_name):
            raise argparse.ArgumentTypeError("TAG_NAME can have only alphabets and underscore.")
        
        if not re.match("^[a-zA-Z0-9_]+$", tag_value):
            raise argparse.ArgumentTypeError("TAG_VALUE can have only alphabets, numbers, and underscore.")
        
        return tag
