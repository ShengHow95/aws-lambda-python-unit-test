import os
import boto3
import requests
import simplejson as json
from requests_aws4auth import AWS4Auth
from aws_lambda_powertools import Logger, Tracer

# Custom Libraries
from http_helper import HttpResponse
from custom_exceptions import BadRequestError, NotFoundError

# Environment Variables
WEB_ORIGIN = os.environ.get('WEB_ORIGIN')
ES_DOMAIN_ENDPOINT = os.environ.get('ES_DOMAIN_ENDPOINT')

# Get AWS Credentials
CREDENTIALS = boto3.Session().get_credentials()
ACCESS_KEY = CREDENTIALS.access_key
SECRET_ACCESS_KEY = CREDENTIALS.secret_key
AWSAUTH = AWS4Auth(ACCESS_KEY, SECRET_ACCESS_KEY, 'ap-southeast-1', 'es', session_token=CREDENTIALS.token)
HEADERS = { 'Content-Type': 'application/json' }

NON_SORT_KEYWORD_FIELDS = ['title', 'shortDescription', 'longDescription', 'status', 'venue']

logger = Logger()
tracer = Tracer()

@tracer.capture_lambda_handler
def lambda_handler(event, context):
    try:
        eventBody = event.get('body') or '{}'
        requestBody = json.loads(eventBody)

        limit = requestBody.get('limit') or 1000
        nextToken = requestBody.get('nextToken') or 0
        sort = requestBody.get('sort') or {}

        sortField = sort.get('field') or 'title'
        sortDirection = sort.get('direction') or 'asc'

        data = get_events_from_os(sortField, sortDirection, limit, nextToken)

        return HttpResponse(200, origin=WEB_ORIGIN, data=data)
    except Exception as ex:
        tracer.put_annotation('lambda_error', 'true')
        tracer.put_annotation('lambda_name', context.function_name)
        tracer.put_metadata('event', event)
        tracer.put_metadata('message', str(ex))
        logger.exception({'message': str(ex)})
        return HttpResponse(500, origin=WEB_ORIGIN, data={'message': 'Something went wrong. Please try again later.'})

@tracer.capture_method
def get_events_from_os(sortField, sortDirection, limit, nextToken):
    esURL = 'https://' + ES_DOMAIN_ENDPOINT + "/event/_doc/_search"
    query = {
        'bool': {
            'must': [],
            'filter': {'term': {'isDeleted': False}}
        }
    }

    if sortField in NON_SORT_KEYWORD_FIELDS:
        sortField += '.keyword'

    payload = dict()
    payload['query'] = query
    payload['size'] = limit
    payload['sort'] = {sortField: {'order': sortDirection}}
    payload['from'] = nextToken
    payload['_source'] = [
        'eventId', 'title', 'shortDescription', 'seoUrl',
        'displayAdmission', 'eventDate', 'displayDate', 'displayVenue',
        'venue', 'region', 'media', 'category', 'topic', 'status'
    ]

    response = requests.request("GET", esURL, data=json.dumps(payload), headers=HEADERS, auth=AWSAUTH)
    responseText = json.loads(response.text)

    data = dict()
    data['items'] = []

    for hit in responseText.get('hits', {}).get('hits', []):
        print(hit)
        hitSource = hit.get('_source', {})
        data['items'].append(hitSource)
    
    data['total'] = responseText.get('hits', {}).get('total', {}).get('value')
    data['nextToken'] = limit + nextToken if limit == len(data['items']) else nextToken + len(data['items'])

    return data
