#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_stacks.lambda_layer_stack import LambdaLayerStack
from cdk_stacks.admin_lambda_stack import AdminLambdaStack


app = cdk.App()

LambdaLayerStack(app, "A-LambdaLayerStack")
AdminLambdaStack(app, "B-AdminLambdaStack")

app.synth()
