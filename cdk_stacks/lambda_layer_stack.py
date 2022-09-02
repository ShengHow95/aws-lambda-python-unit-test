import os
import subprocess

import aws_cdk as cdk
from aws_cdk import aws_ssm as ssm
from aws_cdk import aws_lambda as lambda_

from constructs import Construct

class LambdaLayerStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda layers
        LambdaBaseLayer = lambda_.LayerVersion(
            self, 'LambdaBaseLayer',
            layer_version_name='LambdaBaseLayer',
            code=self.create_dependencies_layer('./lambda/layers/LambdaBase'),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_8],
            description="Lambda Layer with AwsLambdaPowerTools, SimpleJson, Requests, aws4auth and elasticsearch Dependency",
            removal_policy=cdk.RemovalPolicy.RETAIN
        )

        GenericLayer = lambda_.LayerVersion(
            self, 'GenericLayer',
            layer_version_name='GenericLayer',
            code=lambda_.Code.from_asset('./lambda/layers/Generic'),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_8],
            description="Lambda Layer for common code",
            removal_policy=cdk.RemovalPolicy.RETAIN
        )

        # SSM To Store Layer Version
        ssm.StringParameter(
            self, 'LambdaBaseLayerArn',
            string_value=LambdaBaseLayer.layer_version_arn,
            type=ssm.ParameterType.STRING,
            description='Arn for LambdaBaseLayer',
            parameter_name='LambdaBaseLayerArn'
        )

        ssm.StringParameter(
            self, 'GenericLayerArn',
            string_value=GenericLayer.layer_version_arn,
            type=ssm.ParameterType.STRING,
            description='Arn for GenericLayer',
            parameter_name='GenericLayerArn'
        )

    def create_dependencies_layer(self, localPath):
        main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        while localPath[0] == '.' or localPath[0] == '/':
            localPath = localPath[1:]
        
        layerPath = f'{main_dir}/{localPath}'
        
        if not os.path.exists(f'{layerPath}/python'):
            subprocess.check_call(f'pip install -r {layerPath}/requirements.txt -t {layerPath}/python', shell=True)
        return lambda_.Code.from_asset(layerPath)