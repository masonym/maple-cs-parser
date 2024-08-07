import boto3
from botocore.exceptions import ClientError

def setup_dynamodb_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = 'MapleStoryItems'

    try:
        # Check if the new table already exists
        table = dynamodb.Table(table_name)
        table.load()
        print(f"Table {table_name} already exists.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Table {table_name} does not exist. Creating now...")
            try:
                table = dynamodb.create_table(
                    TableName=table_name,
                    KeySchema=[
                        {'AttributeName': 'sn_id', 'KeyType': 'HASH'},  # Partition key
                        {'AttributeName': 'itemID_termStart', 'KeyType': 'RANGE'}  # Sort key
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'sn_id', 'AttributeType': 'S'},
                        {'AttributeName': 'itemID_termStart', 'AttributeType': 'S'}
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )
                table.wait_until_exists()
                print(f"Table {table_name} created successfully.")
            except ClientError as create_error:
                print(f"Error creating table: {create_error}")
                return None
        else:
            print(f"Unexpected error: {e}")
            return None

    return table

table = setup_dynamodb_table()
