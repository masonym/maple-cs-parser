import boto3
from botocore.exceptions import ClientError

def write_to_dynamodb(table, item_info):
    try:
        table.load()
    except ClientError as e:
        print(f"Error loading table: {e}")
        return

    for sn_id, info in item_info.items():
        item = {
            'itemID': info['itemID'],
            'sn_id': sn_id,
            'name': info['name'],
            'count': info['count'],
            'description': info['description'],
            'price': info['price'],
            'discount': info['discount'],
            'originalPrice': info['originalPrice'],
            'termStart': info['termStart'],
            'termEnd': info['termEnd'],
            'gameWorld': info['gameWorld'],
            'period': info['period']
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
            item['packageContents'] = package_contents
        
        try:
            table.put_item(Item=item)
            print(f"Successfully wrote item {sn_id} to DynamoDB.")
        except ClientError as e:
            print(f"Error putting item {sn_id}: {e}")
            continue
    
    print(f"Finished writing {len(item_info)} items to DynamoDB.")