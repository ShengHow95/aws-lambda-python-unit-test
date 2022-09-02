import os
import uuid
import boto3
import simplejson as json
from datetime import datetime
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools import Logger, Tracer

# Custom Libraries
from enum_helper import EventStatus
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
        eventBody = event.get('body') or '{}'
        requestBody = json.loads(eventBody)

        event_ = {
            'eventId': str(uuid.uuid4()),

            'title': requestBody.get('title'),
            'shortDescription': requestBody.get('shortDescription'),
            'longDescription': requestBody.get('longDescription'),
            'media': requestBody.get('media'),
            'status': requestBody.get('status'),
            'isHighlighted': requestBody.get('isHighlighted'),

            'region': requestBody.get('region'),
            'venue': requestBody.get('venue'),
            'displayVenue': requestBody.get('displayVenue'),
            'eventDate': requestBody.get('eventDate'),
            'displayDate': requestBody.get('displayDate'),
            'openingHours': requestBody.get('openingHours'),
            'admission': requestBody.get('admission'),
            'displayAdmission': requestBody.get('displayAdmission'),

            'organizer': requestBody.get('organizer'),
            'category': requestBody.get('category'),
            'topic': requestBody.get('tag'),

            'seoUrl': requestBody.get('seoUrl'),
            'ticketUrl': requestBody.get('ticketUrl'),
            'websiteUrl': requestBody.get('websiteUrl'),
            'facebookUrl': requestBody.get('facebookUrl'),
            'instagramUrl': requestBody.get('instagramUrl'),

            'isDeleted': False,
            'createdAt': now,
            'createdBy': requesterEmail,
            'updatedAt': now,
            'updatedBy': requesterEmail
        }

        if not requestBody or event_.get('status') not in [EventStatus.ACTIVE, EventStatus.INACTIVE]:
            raise BadRequestError('Invalid Parameters')
        
        if check_seourl_existence(event_.get('seoUrl')):
            raise BadRequestError('SeoUrl already exists.')
        
        create_event(event_)

        return HttpResponse(200, origin=WEB_ORIGIN, data=event_)
    except BadRequestError as ex:
        logger.exception({'message': str(ex)})
        return HttpResponse(400, origin=WEB_ORIGIN, data={'message': str(ex)})
    except Exception as ex:
        tracer.put_annotation('lambda_error', 'true')
        tracer.put_annotation('lambda_name', context.function_name)
        tracer.put_metadata('event', event)
        tracer.put_metadata('message', str(ex))
        logger.exception({'message': str(ex)})
        return HttpResponse(500, origin=WEB_ORIGIN, data={'message': 'Something went wrong. Please try again later.'})

@tracer.capture_method
def check_seourl_existence(seoUrl):
    eventResp = EVENT_DDB_TABLE.query(
        IndexName='gsi-seoUrl',
        KeyConditionExpression=Key('seoUrl').eq(seoUrl)
    )

    return eventResp.get('Items')

@tracer.capture_method
def create_event(event_):
    EVENT_DDB_TABLE.put_item(Item=event_)
