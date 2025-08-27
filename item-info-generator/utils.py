import boto3
import os

def get_boto3_session():
    """
    Get a boto3 session using the masonym-dev profile.
    This ensures all AWS calls use the correct credentials.
    """
    # Try to use AWS_PROFILE environment variable if set
    profile_name = os.environ.get('AWS_PROFILE', 'masonym-dev')
    return boto3.Session(profile_name=profile_name)

def get_dynamodb_resource():
    """
    Get a DynamoDB resource using the masonym-dev profile.
    """
    session = get_boto3_session()
    return session.resource('dynamodb')

def format_description(description):
    """
    Format a description string to make it more readable.
    """
    if description:
        return description.replace("#c", "").replace("\\n", "\n").replace("#", "").replace("\\r", "")
    return None

def get_gender_from_id(nItemID):
    nItemID = int(nItemID)
    if nItemID // 1000000 != 1:
        return 2
    switch = nItemID // 1000 % 10
    if switch == 0:
        return 0
    elif switch == 1:
        return 1
    else:
        return 2