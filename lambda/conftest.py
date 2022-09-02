import os
import sys
import boto3
import pytest
from collections import namedtuple
from moto import mock_dynamodb, mock_s3, mock_sqs
from pathlib import Path

# Include Lambda Layers Library
for directory in os.listdir('lambda/layers'):
    sys.path.append(os.getcwd() + '/lambda/layers/' + directory + '/python/')

# Exclude some cache files
sys.dont_write_bytecode = True

# Environment variable
os.environ['AWS_DEFAULT_REGION'] = 'ap-southeast-1'

# Mocked AWS Credentials for moto, ensure this is done first
@pytest.fixture(scope='module')
def aws_credentials():
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['POWERTOOLS_TRACE_DISABLED'] = "true"

# Fixtures which use the mock aws services
@pytest.fixture(scope='module')
def dynamodb_resource(aws_credentials):
    with mock_dynamodb():
        yield boto3.resource('dynamodb', region_name='ap-southeast-1')

@pytest.fixture(scope='module')
def s3_resource(aws_credentials):
    with mock_s3():
        yield boto3.resource('s3', region_name='us-east-1')

@pytest.fixture(scope='module')
def sqs_resource(aws_credentials):
    with mock_sqs():
        yield boto3.resource('sqs', region_name='ap-southeast-1')

@pytest.fixture(scope='module')
def lambda_context():
    lambda_context = {
        "function_name": "test",
        "memory_limit_in_mb": 1024,
        "invoked_function_arn": "arn:aws:lambda:eu-west-1:809313241:function:test",
        "aws_request_id": "52fdfc07-2182-154f-163f-5f0f9a621d72",
    }

    return namedtuple("LambdaContext", lambda_context.keys())(*lambda_context.values())

@pytest.fixture(autouse=True)
def base_path() -> Path:
    """Get the current folder of the test"""
    return Path(__file__).parent
