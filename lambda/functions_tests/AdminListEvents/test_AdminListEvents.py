import os
import json
import importlib
import requests_mock
from test_data_AdminListEvents import (
    ESResponseWithHits,
    ESResponseWithoutHits,
    EventWithData,
    EventWithoutData,
    SampleLambdaEvent1
)

# Environment Variables
WEB_ORIGIN = 'example.com'
ES_DOMAIN_ENDPOINT = 'search.test.com'

os.environ['WEB_ORIGIN'] = WEB_ORIGIN
os.environ['ES_DOMAIN_ENDPOINT'] = ES_DOMAIN_ENDPOINT

# Required Values
EVENT_TABLE_PK = 'eventId'

class TestAdminGetEvent():
    @requests_mock.Mocker(kw='mock')
    def test_get_events_from_os(self, **kwargs):
        lambda_function = importlib.import_module("lambda.functions.AdminListEvents.lambda_function")

        """ List Event - With Hits """
        kwargs['mock'].get(f'https://{ES_DOMAIN_ENDPOINT}/event/_doc/_search', json=ESResponseWithHits)
        response = lambda_function.get_events_from_os(None, None, 1000, 0)
        assert response['items'] == [hits['_source'] for hits in ESResponseWithHits['hits']['hits']]
        assert response['total'] == len(ESResponseWithHits['hits']['hits'])
        assert response['nextToken'] == len(ESResponseWithHits['hits']['hits'])

        """ List Event - Without Hits """
        kwargs['mock'].get(f'https://{ES_DOMAIN_ENDPOINT}/event/_doc/_search', json=ESResponseWithoutHits)
        response = lambda_function.get_events_from_os(None, None, 1000, 0)
        assert response['items'] == [hits['_source'] for hits in ESResponseWithoutHits['hits']['hits']]
        assert response['total'] == len(ESResponseWithoutHits['hits']['hits'])
        assert response['nextToken'] == len(ESResponseWithoutHits['hits']['hits'])

        """ List Event - With Hits """
        kwargs['mock'].get(f'https://{ES_DOMAIN_ENDPOINT}/event/_doc/_search', json=ESResponseWithHits)
        response = lambda_function.get_events_from_os(None, None, 1000, 0)
        assert response['items'] == [hits['_source'] for hits in ESResponseWithHits['hits']['hits']]
        assert response['total'] == len(ESResponseWithHits['hits']['hits'])
        assert response['nextToken'] == len(ESResponseWithHits['hits']['hits'])

    def test_lambda_handler(self, lambda_context, mocker):
        lambda_function = importlib.import_module("lambda.functions.AdminListEvents.lambda_function")

        """ Two Events Returned """
        mocker.patch('lambda.functions.AdminListEvents.lambda_function.get_events_from_os', return_value=EventWithData)
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 200
        assert json.loads(response['body']) == EventWithData

        """ No Event Returned """
        mocker.patch('lambda.functions.AdminListEvents.lambda_function.get_events_from_os', return_value=EventWithoutData)
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 200
        assert json.loads(response['body']) == EventWithoutData

        """ Get Event From OS Throws Error """
        mocker.patch('lambda.functions.AdminListEvents.lambda_function.get_events_from_os', side_effect=Exception())
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 500
        assert json.loads(response['body'])['message'] == 'Something went wrong. Please try again later.'
