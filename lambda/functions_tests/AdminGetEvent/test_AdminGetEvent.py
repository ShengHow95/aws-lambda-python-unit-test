import os
import json
import importlib
from custom_exceptions import NotFoundError
from mock_services_setup.dynamodb_mock import DynamoDB_Table_Mock, DynamoDB_Get_Item
from test_data_AdminGetEvent import (
    InitialEventData,
    SampleLambdaEvent1,
    SampleLambdaEvent2,
    SampleLambdaEvent3
)

# Environment Variables
WEB_ORIGIN = 'example.com'
EVENT_TABLE = 'Event'

os.environ['WEB_ORIGIN'] = WEB_ORIGIN
os.environ['EVENT_TABLE'] = EVENT_TABLE

# Required Values
EVENT_TABLE_PK = 'eventId'

class TestAdminGetEvent():
    def test_create_dynamodb_tables(self, dynamodb_resource):
        globalSecondaryIndexes = ['gsi-seoUrl']
        EventTable = DynamoDB_Table_Mock(dynamodb_resource, EVENT_TABLE, EVENT_TABLE_PK, globalSecondaryIndexes, InitialEventData)
        assert EventTable.name == EVENT_TABLE
        assert EventTable.global_secondary_indexes[0]['IndexName'] == globalSecondaryIndexes[0]

    def test_getEvent(self, dynamodb_resource):
        lambda_function = importlib.import_module("lambda.functions.AdminGetEvent.lambda_function")

        """ Get Event - Success """
        response = lambda_function.get_event('test1')
        data = DynamoDB_Get_Item(dynamodb_resource, EVENT_TABLE, EVENT_TABLE_PK, 'test1')
        assert data == response

        """ Get Event - Failed (Event Not Exists) """
        try:
            response = lambda_function.get_event('test3')
            assert False
        except:
            assert True

        """ Get Event - Failed (eventId is None) """
        try:
            response = lambda_function.get_event(None)
            assert False
        except:
            assert True

        """ Get Event - Failed (eventId is Empty String) """
        try:
            response = lambda_function.get_event('')
            assert False
        except:
            assert True

    def test_lambda_handler(self, lambda_context, mocker):
        lambda_function = importlib.import_module("lambda.functions.AdminGetEvent.lambda_function")

        """ All OK """
        mocker.patch('lambda.functions.AdminGetEvent.lambda_function.get_event', return_value=InitialEventData[0])
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 200
        assert json.loads(response['body']) == InitialEventData[0]

        """ eventId is Empty String """
        mocker.patch('lambda.functions.AdminGetEvent.lambda_function.get_event', return_value=None)
        response = lambda_function.lambda_handler(SampleLambdaEvent2, lambda_context)
        assert response['statusCode'] == 400
        assert json.loads(response['body'])['message'] == 'Invalid Parameters'

        """ eventId is None """
        mocker.patch('lambda.functions.AdminGetEvent.lambda_function.get_event', return_value=None)
        response = lambda_function.lambda_handler(SampleLambdaEvent3, lambda_context)
        assert response['statusCode'] == 400
        assert json.loads(response['body'])['message'] == 'Invalid Parameters'

        """ Event Not Found """
        mocker.patch('lambda.functions.AdminGetEvent.lambda_function.get_event', side_effect=NotFoundError('Event Not Found.'))
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 404
        assert json.loads(response['body'])['message'] == 'Event Not Found.'

        """ Get Event Throws Error """
        mocker.patch('lambda.functions.AdminGetEvent.lambda_function.get_event', side_effect=Exception)
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 500
        assert json.loads(response['body'])['message'] == 'Something went wrong. Please try again later.'
