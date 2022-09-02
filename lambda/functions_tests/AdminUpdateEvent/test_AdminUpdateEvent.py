import os
import json
import importlib
from mock_services_setup.dynamodb_mock import DynamoDB_Table_Mock, DynamoDB_Get_Item
from test_data_AdminUpdateEvent import (
    InitialEventData,
    SampleUpdatedEvent1,
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
    
    def test_checkSeoUrlExistence(self, dynamodb_resource):
        lambda_function = importlib.import_module("lambda.functions.AdminUpdateEvent.lambda_function")

        """ SeoUrl Not Exists """
        response = lambda_function.checkSeoUrlExistence('test', 'test')
        assert response == []

        """ SeoUrl Exists """
        response = lambda_function.checkSeoUrlExistence('test1', 'test2')
        data = DynamoDB_Get_Item(dynamodb_resource, EVENT_TABLE, EVENT_TABLE_PK, 'test2')
        assert response != []
        assert response == [data]

        response = lambda_function.checkSeoUrlExistence('test2', 'test1')
        data = DynamoDB_Get_Item(dynamodb_resource, EVENT_TABLE, EVENT_TABLE_PK, 'test1')
        assert response != []
        assert response == [data]

    def test_update_event(self, dynamodb_resource):
        lambda_function = importlib.import_module("lambda.functions.AdminUpdateEvent.lambda_function")

        """ Update Event - Success """
        lambda_function.update_event(
            SampleUpdatedEvent1['eventId'], SampleUpdatedEvent1['title'], SampleUpdatedEvent1['shortDescription'], 
            SampleUpdatedEvent1['longDescription'], SampleUpdatedEvent1['media'], SampleUpdatedEvent1['status'], SampleUpdatedEvent1['displayVenue'],
            SampleUpdatedEvent1['isHighlighted'], SampleUpdatedEvent1['venue'], SampleUpdatedEvent1['region'], SampleUpdatedEvent1['eventDate'],
            SampleUpdatedEvent1['displayDate'], SampleUpdatedEvent1['openingHours'], SampleUpdatedEvent1['admission'], SampleUpdatedEvent1['category'],
            SampleUpdatedEvent1['topic'], SampleUpdatedEvent1['seoUrl'], SampleUpdatedEvent1['ticketUrl'], SampleUpdatedEvent1['websiteUrl'],
            SampleUpdatedEvent1['displayAdmission'], SampleUpdatedEvent1['organizer'], SampleUpdatedEvent1['facebookUrl'], SampleUpdatedEvent1['instagramUrl'],
            SampleUpdatedEvent1['requesterEmail'], SampleUpdatedEvent1['now']
        )
        data = DynamoDB_Get_Item(dynamodb_resource, EVENT_TABLE, EVENT_TABLE_PK, 'test1')
        assert data['eventId'] == SampleUpdatedEvent1['eventId']
        assert data['title'] == SampleUpdatedEvent1['title']
        assert data['shortDescription'] == SampleUpdatedEvent1['shortDescription']
        assert data['longDescription'] == SampleUpdatedEvent1['longDescription']
        assert data['media'] == SampleUpdatedEvent1['media']
        assert data['status'] == SampleUpdatedEvent1['status']
        assert data['displayVenue'] == SampleUpdatedEvent1['displayVenue']
        assert data['isHighlighted'] == SampleUpdatedEvent1['isHighlighted']
        assert data['venue'] == SampleUpdatedEvent1['venue']
        assert data['region'] == SampleUpdatedEvent1['region']
        assert data['eventDate'] == SampleUpdatedEvent1['eventDate']
        assert data['displayDate'] == SampleUpdatedEvent1['displayDate']
        assert data['openingHours'] == SampleUpdatedEvent1['openingHours']
        assert data['admission'] == SampleUpdatedEvent1['admission']
        assert data['category'] == SampleUpdatedEvent1['category']
        assert data['topic'] == SampleUpdatedEvent1['topic']
        assert data['seoUrl'] == SampleUpdatedEvent1['seoUrl']
        assert data['ticketUrl'] == SampleUpdatedEvent1['ticketUrl']
        assert data['websiteUrl'] == SampleUpdatedEvent1['websiteUrl']
        assert data['displayAdmission'] == SampleUpdatedEvent1['displayAdmission']
        assert data['organizer'] == SampleUpdatedEvent1['organizer']
        assert data['facebookUrl'] == SampleUpdatedEvent1['facebookUrl']
        assert data['instagramUrl'] == SampleUpdatedEvent1['instagramUrl']
        assert data['updatedAt'] == SampleUpdatedEvent1['now']
        assert data['updatedBy'] == SampleUpdatedEvent1['requesterEmail']

        """ Update Event - Failed (eventId is None) """
        try:
            lambda_function.update_event(
                None, 'test', 'test', 'test', 'test', 'test', 'test',
                'test', 'test', 'test', 'test', 'test', 'test', 'test', 
                'test', 'test', 'test', 'test', 'test', 'test', 'test',
                'test', 'test', 'test', 'test'
            )
            assert False
        except:
            assert True

        """ Update Event - Failed (eventId is Empty String) """
        try:
            lambda_function.update_event(
                '', 'test', 'test', 'test', 'test', 'test', 'test',
                'test', 'test', 'test', 'test', 'test', 'test', 'test', 
                'test', 'test', 'test', 'test', 'test', 'test', 'test',
                'test', 'test', 'test', 'test'
            )
            assert False
        except:
            assert True

    def test_lambda_handler(self, lambda_context, mocker):
        lambda_function = importlib.import_module("lambda.functions.AdminUpdateEvent.lambda_function")

        """ All OK """
        mocker.patch('lambda.functions.AdminUpdateEvent.lambda_function.checkSeoUrlExistence', return_value=[])
        mocker.patch('lambda.functions.AdminUpdateEvent.lambda_function.update_event', return_value=json.loads(SampleLambdaEvent1['body']))
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 200
        assert json.loads(response['body']) == json.loads(SampleLambdaEvent1['body'])

        """ eventId is Empty String """
        mocker.patch('lambda.functions.AdminUpdateEvent.lambda_function.checkSeoUrlExistence', return_value=[])
        mocker.patch('lambda.functions.AdminUpdateEvent.lambda_function.update_event', return_value=json.loads(SampleLambdaEvent1['body']))
        response = lambda_function.lambda_handler(SampleLambdaEvent2, lambda_context)
        assert response['statusCode'] == 400
        assert json.loads(response['body'])['message'] == 'Invalid Parameters'

        """ eventId is None """
        mocker.patch('lambda.functions.AdminUpdateEvent.lambda_function.checkSeoUrlExistence', return_value=[])
        mocker.patch('lambda.functions.AdminUpdateEvent.lambda_function.update_event', return_value=json.loads(SampleLambdaEvent1['body']))
        response = lambda_function.lambda_handler(SampleLambdaEvent3, lambda_context)
        assert response['statusCode'] == 400
        assert json.loads(response['body'])['message'] == 'Invalid Parameters'

        """ SeoUrl Exists """
        mocker.patch('lambda.functions.AdminUpdateEvent.lambda_function.checkSeoUrlExistence', return_value=InitialEventData)
        mocker.patch('lambda.functions.AdminUpdateEvent.lambda_function.update_event', return_value=json.loads(SampleLambdaEvent1['body']))
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 400
        assert json.loads(response['body'])['message'] == 'SeoUrl already exists.'

        """ Update Event Throws Exception """
        mocker.patch('lambda.functions.AdminUpdateEvent.lambda_function.checkSeoUrlExistence', return_value=[])
        mocker.patch('lambda.functions.AdminUpdateEvent.lambda_function.update_event', side_effect=Exception())
        response = lambda_function.lambda_handler(SampleLambdaEvent1, lambda_context)
        assert response['statusCode'] == 500
        assert json.loads(response['body'])['message'] == 'Something went wrong. Please try again later.'
