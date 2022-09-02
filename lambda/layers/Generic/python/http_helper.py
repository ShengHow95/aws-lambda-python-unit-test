import simplejson as json
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

@tracer.capture_method
def HttpResponse(statusCode, *, origin, data={}):
    return {
        'statusCode': statusCode,
        'headers': {
            'content-type': 'application/json',
            'strict-transport-security': 'max-age=31536000;includeSubDomains',
            'x-xss-protection': '1; mode=block',
            'x-content-type-options': 'nosniff',
            'x-frame-options': 'sameorigin',
            'content-security-policy': 'script-src "self"',
            'referrer-policy': 'no-referrer',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
        },
        'body': json.dumps(data, use_decimal=True)
    }