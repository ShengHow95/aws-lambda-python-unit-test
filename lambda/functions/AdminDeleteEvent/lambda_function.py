import os
import boto3
from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from aws_lambda_powertools import Logger, Tracer

# Custom Libraries
from http_helper import HttpResponse
from custom_exceptions import BadRequestError

# Environment Variables
WEB_ORIGIN = os.environ.get('WEB_ORIGIN')
EVENT_TABLE = os.environ.get('EVENT_TABLE')

# AWS Client or Resource
DDB_RESOURCE = boto3.resource('dynamodb')

EVENT_DDB_TABLE = DDB_RESOURCE.Table(EVENT_TABLE)

logger = Logger()
tracer = Tracer()

@tracer.capture_lambda_handler
def lambda_handler(event, context):
    try:
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        requesterEmail = event.get('requestContext', {}).get('authorizer', {}).get('claims', {}).get('email')
        queryStringParameters = event.get('queryStringParameters') or {}
        eventId = queryStringParameters.get('eventId')

        if not queryStringParameters or not eventId:
            raise BadRequestError('Invalid Parameters')
        
        delete_event(eventId, requesterEmail, now)
        return HttpResponse(200, origin=WEB_ORIGIN, data={'message': 'Successfully deleted Event.'})
    except BadRequestError as ex:
        return HttpResponse(400, origin=WEB_ORIGIN, data={'message': str(ex)})
    except Exception as ex:
        tracer.put_annotation('lambda_error', 'true')
        tracer.put_annotation('lambda_name', context.function_name)
        tracer.put_metadata('event', event)
        tracer.put_metadata('message', str(ex))
        logger.exception({'message': str(ex)})
        return HttpResponse(500, origin=WEB_ORIGIN, data={'message': 'Something went wrong. Please try again later.'})

@tracer.capture_method
def delete_event(eventId, requesterEmail, now):
    EVENT_DDB_TABLE.update_item(
        Key={'eventId': eventId},
        UpdateExpression='SET isDeleted=:isDeleted, updatedAt=:updatedAt, updatedBy=:updatedBy',
        ExpressionAttributeValues={
            ':isDeleted': True,
            ':updatedAt': now,
            ':updatedBy': requesterEmail
        }
    )
