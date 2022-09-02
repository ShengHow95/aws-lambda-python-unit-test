import os
import boto3
import simplejson as json
from decimal import Decimal
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

@tracer.capture_method
def DeleteCacheValue(redisClient, cacheKey):
    redisClient.delete(cacheKey)

@tracer.capture_method     
def GetCacheValue(redisClient, cacheKey):
    cacheValue = redisClient.get(cacheKey)
    if cacheValue:
        return json.loads(cacheValue)
    else:
        return None

@tracer.capture_method
def SetCacheValue(redisClient, cacheKey, cacheValue):
    redisClient.set(cacheKey, json.dumps(cacheValue, use_decimal=True))
    return cacheValue
