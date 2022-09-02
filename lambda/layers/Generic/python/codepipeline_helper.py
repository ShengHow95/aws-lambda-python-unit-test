import os
import boto3
from aws_lambda_powertools import Logger, Tracer

CODE_PIPELINE_CLIENT = boto3.client('codepipeline')

logger = Logger()
tracer = Tracer()

@tracer.capture_method
def triggerPublicWebRegeneration(pipelineName):
    CODE_PIPELINE_CLIENT.start_pipeline_execution(name=pipelineName)
