import os
import boto3
import simplejson as json
from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
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

        eventId = requestBody.get('eventId')
        title = requestBody.get('title')
        shortDescription = requestBody.get('shortDescription')
        longDescription = requestBody.get('longDescription')
        media = requestBody.get('media')
        status = requestBody.get('status')
        isHighlighted = requestBody.get('isHighlighted')
        venue = requestBody.get('venue')
        displayVenue = requestBody.get('displayVenue')
        region = requestBody.get('region')
        eventDate = requestBody.get('eventDate')
        displayDate = requestBody.get('displayDate')
        openingHours = requestBody.get('openingHours')
        admission = requestBody.get('admission')
        displayAdmission = requestBody.get('displayAdmission')
        organizer = requestBody.get('organizer')
        category = requestBody.get('category')
        topic = requestBody.get('topic')
        seoUrl = requestBody.get('seoUrl')
        ticketUrl = requestBody.get('ticketUrl')
        websiteUrl = requestBody.get('websiteUrl')
        facebookUrl = requestBody.get('facebookUrl')
        instagramUrl = requestBody.get('instagramUrl')

        if not requestBody or not eventId or status not in [EventStatus.ACTIVE, EventStatus.INACTIVE]:
            raise BadRequestError('Invalid Parameters')
        
        if check_seourl_existence(eventId, seoUrl):
            raise BadRequestError('SeoUrl already exists.')

        event = update_event(
            eventId, title, shortDescription, longDescription, media, status, displayVenue,
            isHighlighted, venue, region, eventDate, displayDate, openingHours, admission, 
            category, topic, seoUrl, ticketUrl, websiteUrl, displayAdmission, organizer,
            facebookUrl, instagramUrl, requesterEmail, now
        )

        return HttpResponse(200, origin=WEB_ORIGIN, data=event)
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
def check_seourl_existence(eventId, seoUrl):
    eventResp = EVENT_DDB_TABLE.query(
        IndexName='gsi-seoUrl',
        KeyConditionExpression=Key('seoUrl').eq(seoUrl),
        FilterExpression=Attr('eventId').ne(eventId)
    )
    
    return eventResp.get('Items')

@tracer.capture_method
def update_event(
    eventId, title, shortDescription, longDescription, media, status, displayVenue,
    isHighlighted, venue, region, eventDate, displayDate, openingHours, admission, 
    category, topic, seoUrl, ticketUrl, websiteUrl, displayAdmission, organizer,
    facebookUrl, instagramUrl, requesterEmail, now
):
    updateExpression = 'SET #title=:title, #shortDescription=:shortDescription, #longDescription=:longDescription, #media=:media, #status=:status, #displayVenue=:displayVenue'
    updateExpression += ', #isHighlighted=:isHighlighted, #venue=:venue, #region=:region, #eventDate=:eventDate, #displayDate=:displayDate, #openingHours=:openingHours'
    updateExpression += ', #admission=:admission, #category=:category, #topic=:topic, #seoUrl=:seoUrl, #organizer=:organizer'
    updateExpression += ', #ticketUrl=:ticketUrl, #websiteUrl=:websiteUrl, #facebookUrl=:facebookUrl, #instagramUrl=:instagramUrl'
    updateExpression += ', #updatedAt=:updatedAt, #updatedBy=:updatedBy, #displayAdmission=:displayAdmission'

    expressionAttributeNames = {
        '#title': 'title',
        '#shortDescription': 'shortDescription',
        '#longDescription': 'longDescription',
        '#media': 'media',
        '#status': 'status',
        '#isHighlighted': 'isHighlighted',
        '#venue': 'venue',
        '#displayVenue': 'displayVenue',
        '#region': 'region',
        '#eventDate': 'eventDate',
        '#displayDate': 'displayDate',
        '#openingHours': 'openingHours',
        '#admission': 'admission',
        '#displayAdmission': 'displayAdmission',
        '#organizer': 'organizer',
        '#category': 'category',
        '#topic': 'topic',
        '#seoUrl': 'seoUrl',
        '#ticketUrl': 'ticketUrl',
        '#websiteUrl': 'websiteUrl',
        '#facebookUrl': 'facebookUrl',
        '#instagramUrl': 'instagramUrl',
        '#updatedAt': 'updatedAt',
        '#updatedBy': 'updatedBy'
    }

    expressionAttributeValues = {
        ':title': title,
        ':shortDescription': shortDescription,
        ':longDescription': longDescription,
        ':media': media,
        ':status': status,
        ':isHighlighted': isHighlighted,
        ':venue': venue,
        ':displayVenue': displayVenue,
        ':region': region,
        ':eventDate': eventDate,
        ':displayDate': displayDate,
        ':openingHours': openingHours,
        ':admission': admission,
        ':displayAdmission': displayAdmission,
        ':organizer': organizer,
        ':category': category,
        ':topic': topic,
        ':seoUrl': seoUrl,
        ':ticketUrl': ticketUrl,
        ':websiteUrl': websiteUrl,
        ':facebookUrl': facebookUrl,
        ':instagramUrl': instagramUrl,
        ':updatedAt': now,
        ':updatedBy': requesterEmail
    }

    eventResp = EVENT_DDB_TABLE.update_item(
        Key={'eventId': eventId},
        UpdateExpression=updateExpression,
        ExpressionAttributeNames=expressionAttributeNames,
        ExpressionAttributeValues=expressionAttributeValues,
        ReturnValues='ALL_NEW'
    )

    event = eventResp.get('Attributes')
    if not event:
        raise Exception('Failed to update Event.')
    
    return event
