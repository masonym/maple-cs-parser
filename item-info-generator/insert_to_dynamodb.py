import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
from utils import get_dynamodb_resource

dynamodb = get_dynamodb_resource()
table = dynamodb.Table('MapleStoryItems')

def parse_date(date_str):
    return datetime.strptime(date_str, '%m-%d-%Y %H:%M UTC')

def format_date(date):
    return date.strftime('%m-%d-%Y %H:%M UTC')

def get_current_utc_time():
    return format_date(datetime.utcnow())

def get_last_seen(item_id):
    try:
        response = table.query(
            IndexName='itemID-termStart-index',  # Assuming you have this GSI
            KeyConditionExpression=boto3.dynamodb.conditions.Key('itemID').eq(item_id),
            ScanIndexForward=False,  # This will sort in descending order
            Limit=1
        )
        items = response.get('Items', [])
        if items:
            return items[0]['termStart']
        return None
    except ClientError as e:
        print(f"Error querying for last seen of item {item_id}: {e}")
        return None

def write_to_dynamodb(item_info):
    try:
        for sn_id, info in item_info.items():
            item_id = info['itemID']
            term_start = info['termStart']

            last_seen = get_last_seen(item_id)
            
            last_seen_display = last_seen if last_seen else "First seen"

            new_item = {
                'sn_id': sn_id,
                'itemID_termStart': f"{item_id}_{term_start}",
                'itemID': item_id,
                'name': info['name'],
                'count': info['count'],
                'description': info['description'],
                'price': info['price'],
                'discount': info['discount'],
                'originalPrice': info['originalPrice'],
                'termStart': term_start,
                'termEnd': info['termEnd'],
                'gameWorld': info['gameWorld'],
                'period': info['period'],
                'lastSeen': last_seen_display
            }

            if 'packageContents' in info:
                package_contents = []
                for package_id, contents in info['packageContents'].items():
                    for content_id, content_info in contents.items():
                        package_contents.append({
                            'itemID': content_info['itemID'],
                            'name': content_info['name'],
                            'description': content_info['description'],
                            'count': content_info['count'],
                            'period': content_info['period']
                        })
                new_item['packageContents'] = package_contents

            try:
                table.put_item(Item=new_item)
                print(f"Successfully wrote item {sn_id} to DynamoDB.")
            except ClientError as e:
                print(f"Error putting item {sn_id}: {e}")
                continue

        print(f"Finished writing {len(item_info)} items to DynamoDB.")
    except ClientError as e:
        print(f"Error processing items: {e}")