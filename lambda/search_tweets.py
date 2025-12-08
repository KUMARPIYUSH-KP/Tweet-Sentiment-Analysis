import json
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('TweetsDatabase')

# Helper to convert Decimal to native types
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def lambda_handler(event, context):
    """
    Search tweets by keyword and return specified number of results
    
    Expected input:
    {
        "keyword": "pizza",
        "limit": 50
    }
    """
    
    try:
        # Parse input
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        keyword = body.get('keyword', '').lower().strip()
        limit = int(body.get('limit', 50))
        
        # Validate input
        if not keyword:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({
                    'error': 'Keyword is required',
                    'success': False
                })
            }
        
        if limit < 1 or limit > 1000:
            limit = 50  # Default to 50 if invalid
        
        # Scan DynamoDB table with filter
        print(f"Searching for keyword: {keyword}, limit: {limit}")
        
        response = table.scan(
            FilterExpression=Attr('tweet_text').contains(keyword) | 
                           Attr('tweet_text').contains(keyword.capitalize()) |
                           Attr('tweet_text').contains(keyword.upper()),
            Limit=limit * 3  # Scan more items to ensure we get enough matches
        )
        
        items = response.get('Items', [])
        
        # Continue scanning if we need more items
        while len(items) < limit and 'LastEvaluatedKey' in response:
            response = table.scan(
                FilterExpression=Attr('tweet_text').contains(keyword) |
                               Attr('tweet_text').contains(keyword.capitalize()) |
                               Attr('tweet_text').contains(keyword.upper()),
                ExclusiveStartKey=response['LastEvaluatedKey'],
                Limit=limit * 3
            )
            items.extend(response.get('Items', []))
        
        # Limit results
        items = items[:limit]
        
        print(f"Found {len(items)} tweets matching '{keyword}'")
        
        # Return results
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'success': True,
                'count': len(items),
                'keyword': keyword,
                'tweets': items
            }, default=decimal_default)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'error': str(e),
                'success': False
            })
        }