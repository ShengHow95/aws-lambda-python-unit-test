import os
import json
import importlib
from mock_services_setup.dynamodb_mock import DynamoDB_Table_Mock, DynamoDB_Get_Item
from test_data_AdminCreateEvent import (
    InitialEventData,
    SampleEvent1,
    SampleEvent2,
    SampleEvent3,
    SampleLambdaEvent1,
    SampleLambdaEvent2
)

# Environment Variables
WEB_ORIGIN = 'example.com'
EVENT_TABLE = 'Event'

os.environ['WEB_ORIGIN'] = WEB_ORIGIN
os.environ['EVENT_TABLE'] = EVENT_TABLE

# Required Values
EVENT_TABLE_PK = 'eventId'

class TestAdminCreateEvent():
    def test_create_dynamodb_tables(self, dynamodb_resource):
        globalSecondaryIndexes = ['gsi-seoUrl']
        EventTable = DynamoDB_Table_Mock(dynamodb_resource, EVENT_TABLE, EVENT_TABLE_PK, globalSecondaryIndexes, InitialEventData)
        assert EventTable.name == EVENT_TABLE
        assert EventTable.global_secondary_indexes[0]['IndexName'] == globalSecondaryIndexes[0]

    def test_check_seourl_existence(self, dynamodb_resource):
        lambda_function = importlib.import_module("lambda.functions.AdminCreateEvent.lambda_function")

        """ SeoUrl Not Exists """
        response = lambda_function.check_seourl_existence('test')
        assert response == []

        """ SeoUrl Exists """
        response = lambda_function.check_seourl_existence('test1')
        data = DynamoDB_Get_Item(dynamodb_resource, EVENT_TABLE, EVENT_TABLE_PK, 'test1')
        assert response != []
        assert response == [data]

        response = lambda_function.check_seourl_existence('test2')
        data = DynamoDB_Get_Item(dynamodb_resource, EVENT_TABLE, EVENT_TABLE_PK, 'test2')
        assert response != []
        assert response == [data]
    
    def test_createEvent(self, dynamodb_resource):
        lambda_function = importlib.import_module("lambda.functions.AdminCreateEvent.lambda_function")

        """ Create Event (Success - Any Payload) """
        response = lambda_function.create_event(SampleEvent1)
        data = DynamoDB_Get_Item(dynamodb_resource, EVENT_TABLE, EVENT_TABLE_PK, 'test3')
        assert response == None
        assert data == SampleEvent1

        """ Create Event (Failed - eventId is None) """
        try:
            response = lambda_function.create_event(SampleEvent2)
            assert False
        except:
            assert True

        """ Create Event (Failed - seoUrl is None) """
        try:
            response = lambda_function.create_event(SampleEvent3)
            assert False
        except:
            assert True

    def test_lambda_handler(self, lambda_context, mocker):
        lambda_function = importlib.import_module("lambda.functions.AdminCreateEvent.lambda_function")

        """ All OK """
        mocker.patch('lambda.functions.AdminCreateEvent.lambda_function.check_seourl_existence', return_value=[])
        mocker.patch('lambda.functions.AdminCreateEvent.lambda_function.create_event', return_value=None)
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 200
        assert isinstance(json.loads(response['body'])['eventId'], str)

        """ Event Status not ACTIVE or INACTIVE """
        mocker.patch('lambda.functions.AdminCreateEvent.lambda_function.check_seourl_existence', return_value=[])
        mocker.patch('lambda.functions.AdminCreateEvent.lambda_function.create_event', return_value=None)
        response = lambda_function.lambda_handler(SampleLambdaEvent2, lambda_context)
        assert response['statusCode'] == 400
        assert json.loads(response['body'])['message'] == 'Invalid Parameters'

        """ SeoUrl Already Exists """
        mocker.patch('lambda.functions.AdminCreateEvent.lambda_function.check_seourl_existence', return_value=InitialEventData)
        mocker.patch('lambda.functions.AdminCreateEvent.lambda_function.create_event', return_value=None)
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 400
        assert json.loads(response['body'])['message'] == 'SeoUrl already exists.'

        """ Create Event Throws Exception """
        mocker.patch('lambda.functions.AdminCreateEvent.lambda_function.check_seourl_existence', return_value=[])
        mocker.patch('lambda.functions.AdminCreateEvent.lambda_function.create_event', side_effect=Exception())
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 500
        assert json.loads(response['body'])['message'] == 'Something went wrong. Please try again later.'
