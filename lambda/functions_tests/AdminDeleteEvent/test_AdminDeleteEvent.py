import os
import json
import importlib
from mock_services_setup.dynamodb_mock import DynamoDB_Table_Mock, DynamoDB_Get_Item
from test_data_AdminDeleteEvent import (
    InitialEventData,
    SampleDeleteEvent1,
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

class TestAdminDeleteEvent():
    def test_create_dynamodb_tables(self, dynamodb_resource):
        globalSecondaryIndexes = ['gsi-seoUrl']
        EventTable = DynamoDB_Table_Mock(dynamodb_resource, EVENT_TABLE, EVENT_TABLE_PK, globalSecondaryIndexes, InitialEventData)
        assert EventTable.name == EVENT_TABLE
        assert EventTable.global_secondary_indexes[0]['IndexName'] == globalSecondaryIndexes[0]

    def test_deleteEvent(self, dynamodb_resource):
        lambda_function = importlib.import_module("lambda.functions.AdminDeleteEvent.lambda_function")

        """ Delete Event - Success """
        response = lambda_function.delete_event(SampleDeleteEvent1['eventId'], SampleDeleteEvent1['requesterEmail'], SampleDeleteEvent1['now'])
        data = DynamoDB_Get_Item(dynamodb_resource, EVENT_TABLE, EVENT_TABLE_PK, SampleDeleteEvent1['eventId'])
        assert response == None
        assert data['eventId'] == SampleDeleteEvent1['eventId']
        assert data['updatedBy'] == SampleDeleteEvent1['requesterEmail']
        assert data['updatedAt'] == SampleDeleteEvent1['now']
        assert data['isDeleted'] == True

        """ Delete Event - Failed (eventId is None) """
        try:
            response = lambda_function.delete_event(None, SampleDeleteEvent1['requesterEmail'], SampleDeleteEvent1['now'])
            assert False
        except:
            assert True

    def test_lambda_handler(self, lambda_context, mocker):
        lambda_function = importlib.import_module("lambda.functions.AdminDeleteEvent.lambda_function")

        """ All OK """
        mocker.patch('lambda.functions.AdminDeleteEvent.lambda_function.delete_event', return_value=None)
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 200
        assert json.loads(response['body'])['message'] == 'Successfully deleted Event.'

        """ eventId is Empty String """
        mocker.patch('lambda.functions.AdminDeleteEvent.lambda_function.delete_event', return_value=None)
        response = lambda_function.lambda_handler(SampleLambdaEvent2, lambda_context)
        assert response['statusCode'] == 400
        assert json.loads(response['body'])['message'] == 'Invalid Parameters'

        """ eventId is None """
        mocker.patch('lambda.functions.AdminDeleteEvent.lambda_function.delete_event', return_value=None)
        response = lambda_function.lambda_handler(SampleLambdaEvent3, lambda_context)
        assert response['statusCode'] == 400
        assert json.loads(response['body'])['message'] == 'Invalid Parameters'

        """ Delete Event Throws Exception """
        mocker.patch('lambda.functions.AdminDeleteEvent.lambda_function.delete_event', side_effect=Exception())
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 500
        assert json.loads(response['body'])['message'] == 'Something went wrong. Please try again later.'
