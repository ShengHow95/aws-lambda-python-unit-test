#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_stacks.empty_stack import AwsLambdaPythonUnitTestStack


app = cdk.App()

AwsLambdaPythonUnitTestStack(app, "AwsLambdaPythonUnitTestStack")

app.synth()
