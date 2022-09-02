import aws_cdk as cdk
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ssm as ssm
from aws_cdk import aws_lambda as lambda_

from datetime import datetime
from constructs import Construct

class AdminLambdaStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Parameters
        lambda_dir = './lambda/functions/'
        LambdaBaseLayerArn = ssm.StringParameter.from_string_parameter_name(self, 'LambdaBaseLayerArn', 'LambdaBaseLayerArn').string_value
        GenericLayerArn = ssm.StringParameter.from_string_parameter_name(self, 'GenericLayerArn', 'GenericLayerArn').string_value
        OpenSearchEndpoint = ssm.StringParameter.from_string_parameter_name(self, 'OpenSearchDomainEndpoint', 'OpenSearchDomainEndpoint').string_value

        # Datetime now
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        # IAM Roles
        ApiGatewayAdminLambdaRole = iam.Role(
            self, 'ApiGatewayAdminLambdaRole',
            role_name='ApiGatewayAdminLambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            description='IAM Role to be used by Admin API Gateway Triggered Lambda Functions',
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(self, 'AWSXrayWriteOnlyAccess', 'arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess'),
                iam.ManagedPolicy.from_managed_policy_arn(self, 'AmazonDynamoDBFullAccess', 'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess'),
                iam.ManagedPolicy.from_managed_policy_arn(self, 'AmazonS3FullAccess', 'arn:aws:iam::aws:policy/AmazonS3FullAccess'),
                iam.ManagedPolicy.from_managed_policy_arn(self, 'AmazonOpenSearchServiceFullAccess', 'arn:aws:iam::aws:policy/AmazonOpenSearchServiceFullAccess'),
                iam.ManagedPolicy.from_managed_policy_arn(self, 'AWSLambdaVPCAccessExecutionRole', 'arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole')
            ]
        )

        # Lambda Layers
        LambdaBaseLayer = lambda_.LayerVersion.from_layer_version_arn(
            self, 'LambdaBaseLayer',
            LambdaBaseLayerArn
        )

        GenericLayer = lambda_.LayerVersion.from_layer_version_arn(
            self, 'GenericLayer',
            GenericLayerArn
        )

        # Lambda Functions
        AdminCreateEvent = lambda_.Function(
            self, 'AdminCreateEvent',
            function_name='AdminCreateEvent',
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler='lambda_function.lambda_handler',
            code=lambda_.Code.from_asset(lambda_dir + 'AdminCreateEvent'),
            layers=[LambdaBaseLayer, GenericLayer],
            description="Function to Create Event in Admin Portal",
            role=ApiGatewayAdminLambdaRole.without_policy_updates(),
            environment={
                'WEB_ORIGIN': '*',
                'EVENT_TABLE': 'Event'
            },
            timeout=cdk.Duration.seconds(30),
            tracing=lambda_.Tracing.ACTIVE,
            memory_size=512
        )

        AdminGetEvent = lambda_.Function(
            self, 'AdminGetEvent',
            function_name='AdminGetEvent',
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler='lambda_function.lambda_handler',
            code=lambda_.Code.from_asset(lambda_dir + 'AdminGetEvent'),
            layers=[LambdaBaseLayer, GenericLayer],
            description="Function to Get Event in Admin Portal",
            role=ApiGatewayAdminLambdaRole.without_policy_updates(),
            environment={
                'WEB_ORIGIN': '*',
                'EVENT_TABLE': 'Event'
            },
            timeout=cdk.Duration.seconds(30),
            tracing=lambda_.Tracing.ACTIVE,
            memory_size=512
        )

        AdminUpdateEvent = lambda_.Function(
            self, 'AdminUpdateEvent',
            function_name='AdminUpdateEvent',
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler='lambda_function.lambda_handler',
            code=lambda_.Code.from_asset(lambda_dir + 'AdminUpdateEvent'),
            layers=[LambdaBaseLayer, GenericLayer],
            description="Function to Update Event in Admin Portal",
            role=ApiGatewayAdminLambdaRole.without_policy_updates(),
            environment={
                'WEB_ORIGIN': '*',
                'EVENT_TABLE': 'Event'
            },
            timeout=cdk.Duration.seconds(30),
            tracing=lambda_.Tracing.ACTIVE,
            memory_size=512
        )

        AdminDeleteEvent = lambda_.Function(
            self, 'AdminDeleteEvent',
            function_name='AdminDeleteEvent',
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler='lambda_function.lambda_handler',
            code=lambda_.Code.from_asset(lambda_dir + 'AdminDeleteEvent'),
            layers=[LambdaBaseLayer, GenericLayer],
            description="Function to Delete Event in Admin Portal",
            role=ApiGatewayAdminLambdaRole.without_policy_updates(),
            environment={
                'WEB_ORIGIN': '*',
                'EVENT_TABLE': 'Event'
            },
            timeout=cdk.Duration.seconds(30),
            tracing=lambda_.Tracing.ACTIVE,
            memory_size=512
        )

        AdminListEvents = lambda_.Function(
            self, 'AdminListEvents',
            function_name='AdminListEvents',
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler='lambda_function.lambda_handler',
            code=lambda_.Code.from_asset(lambda_dir + 'AdminListEvents'),
            layers=[LambdaBaseLayer, GenericLayer],
            description="Function to List Events in Admin Portal",
            role=ApiGatewayAdminLambdaRole.without_policy_updates(),
            environment={
                'WEB_ORIGIN': '*',
                'ES_DOMAIN_ENDPOINT': OpenSearchEndpoint
            },
            timeout=cdk.Duration.seconds(30),
            tracing=lambda_.Tracing.ACTIVE,
            memory_size=512
        )
