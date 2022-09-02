from datetime import datetime

InitialEventData = [
    {
        "eventId": "test1",
        "admission": "test1",
        "category": "test1",
        "createdBy": "test1",
        "displayAdmission": "test1",
        "displayDate": "test1",
        "displayVenue": "test1",
        "eventDate": [],
        "facebookUrl": "test1",
        "instagramUrl": "test1",
        "isDeleted": False,
        "isHighlighted": False,
        "longDescription": "test1",
        "media": ["test1.jpg"],
        "openingHours": "test1",
        "organizer": "test1",
        "region": "test1",
        "seoUrl": "test1",
        "shortDescription": "test1",
        "status": "ACTIVE",
        "ticketUrl": "test1",
        "title": "test1",
        "topic": "test1",
        "updatedBy": "test1",
        "venue": "test1",
        "websiteUrl": "test1"
    },
    {
        "eventId": "test2",
        "admission": "test2",
        "category": "test2",
        "createdBy": "test2",
        "displayAdmission": "test2",
        "displayDate": "test2",
        "displayVenue": "test2",
        "eventDate": [],
        "facebookUrl": "test2",
        "instagramUrl": "test2",
        "isDeleted": False,
        "isHighlighted": False,
        "longDescription": "test2",
        "media": ["test2.jpg"],
        "openingHours": "test2",
        "organizer": "test2",
        "region": "test2",
        "seoUrl": "test2",
        "shortDescription": "test2",
        "status": "ACTIVE",
        "ticketUrl": "test2",
        "title": "test2",
        "topic": "test2",
        "updatedBy": "test2",
        "venue": "test2",
        "websiteUrl": "test2"
    }
]

SampleLambdaEvent1 = {
    'queryStringParameters': {
        "eventId": "test1"
    },
    'requestContext': {
        'authorizer': {
            'claims': {
                'email': 'test@test.com'
            }
        }
    }
}

SampleLambdaEvent2 = {
    'queryStringParameters': {
        "eventId": ""
    },
    'requestContext': {
        'authorizer': {
            'claims': {
                'email': 'test@test.com'
            }
        }
    }
}

SampleLambdaEvent3 = {
    'queryStringParameters': {
        "eventId": None
    },
    'requestContext': {
        'authorizer': {
            'claims': {
                'email': 'test@test.com'
            }
        }
    }
}