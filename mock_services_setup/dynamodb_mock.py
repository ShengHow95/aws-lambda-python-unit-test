from contextlib import contextmanager

@contextmanager
def dynamodb_table_setup(dynamodbResource, tableName, partitionKey, globalSecondaryIndexes=[]):
    attributeDefinitions = [{'AttributeName': partitionKey, 'AttributeType': 'S'}]
    
    # GSI Standard Format gsi-xxx-yyy
    gsiConfigs = []
    for gsi in globalSecondaryIndexes:
        gsiAttributes = gsi.split('-')
        gsiSchemas = [{'AttributeName': gsiAttributes[1], 'KeyType': 'HASH'}]
        if gsiAttributes[1] not in [attributeDefinition.get('AttributeName') for attributeDefinition in attributeDefinitions]:
            attributeDefinitions.append({'AttributeName': gsiAttributes[1], 'AttributeType': 'S'})

        if len(gsiAttributes) == 3:
            gsiSchemas.append({'AttributeName': gsiAttributes[2], 'KeyType': 'RANGE'})
            if gsiAttributes[2] not in [attributeDefinition.get('AttributeName') for attributeDefinition in attributeDefinitions]:
                attributeDefinitions.append({'AttributeName': gsiAttributes[2], 'AttributeType': 'S'})

        gsiConfigs.append({
            'IndexName': gsi,
            'KeySchema': gsiSchemas,
            'Projection': {'ProjectionType': 'ALL'}
        })

    if gsiConfigs:
        dynamodbResource.create_table(
            TableName=tableName,
            KeySchema=[{'AttributeName': partitionKey, 'KeyType': 'HASH'}],
            AttributeDefinitions=attributeDefinitions,
            BillingMode='PAY_PER_REQUEST',
            GlobalSecondaryIndexes=gsiConfigs
        )
    else:
        dynamodbResource.create_table(
            TableName=tableName,
            KeySchema=[{'AttributeName': partitionKey, 'KeyType': 'HASH'}],
            AttributeDefinitions=attributeDefinitions,
            BillingMode='PAY_PER_REQUEST'
        )

    yield

def DynamoDB_Table_Mock(dynamodbResource, tableName, partitionKey, globalSecondaryIndexes=[], initialData=[]):
    with dynamodb_table_setup(dynamodbResource, tableName, partitionKey, globalSecondaryIndexes):
        table = dynamodbResource.Table(tableName)
        for item in initialData:
            table.put_item(Item=item)
        return dynamodbResource.Table(tableName)

def DynamoDB_Get_Item(dynamodbResource, tableName, partitionKey, partitionKeyValue):
    table = dynamodbResource.Table(tableName)
    item = table.get_item(Key={partitionKey: partitionKeyValue}).get('Item')
    return item