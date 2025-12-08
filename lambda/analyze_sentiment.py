import json
import boto3
from decimal import Decimal

# Initialize AWS Comprehend
comprehend = boto3.client('comprehend', region_name='ap-south-1')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def analyze_sentiment(text):
    """Analyze sentiment of a single text using AWS Comprehend"""
    try:
        response = comprehend.detect_sentiment(
            Text=text[:5000],  # Comprehend limit is 5000 bytes
            LanguageCode='en'
        )
        return {
            'sentiment': response['Sentiment'],
            'scores': {
                'positive': round(response['SentimentScore']['Positive'], 4),
                'negative': round(response['SentimentScore']['Negative'], 4),
                'neutral': round(response['SentimentScore']['Neutral'], 4),
                'mixed': round(response['SentimentScore']['Mixed'], 4)
            }
        }
    except Exception as e:
        print(f"Error analyzing sentiment: {str(e)}")
        return {
            'sentiment': 'NEUTRAL',
            'scores': {
                'positive': 0.25,
                'negative': 0.25,
                'neutral': 0.25,
                'mixed': 0.25
            },
            'error': str(e)
        }

def lambda_handler(event, context):
    """
    Analyze sentiment for tweets
    
    Expected input:
    {
        "tweets": [
            {"tweet_id": "123", "tweet_text": "I love this!", ...},
            {"tweet_id": "456", "tweet_text": "This is terrible", ...}
        ]
    }
    """
    
    try:
        # Parse input
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        tweets = body.get('tweets', [])
        
        if not tweets:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({
                    'error': 'No tweets provided',
                    'success': False
                })
            }
        
        # Analyze sentiment for each tweet
        analyzed_tweets = []
        
        for tweet in tweets:
            tweet_text = tweet.get('tweet_text', '')
            
            if not tweet_text:
                continue
            
            # Get sentiment analysis
            sentiment_result = analyze_sentiment(tweet_text)
            
            # Add sentiment to tweet data
            tweet_with_sentiment = tweet.copy()
            tweet_with_sentiment['analyzed_sentiment'] = sentiment_result['sentiment']
            tweet_with_sentiment['sentiment_scores'] = sentiment_result['scores']
            
            analyzed_tweets.append(tweet_with_sentiment)
        
        # Calculate summary statistics
        sentiment_counts = {
            'POSITIVE': 0,
            'NEGATIVE': 0,
            'NEUTRAL': 0,
            'MIXED': 0
        }
        
        for tweet in analyzed_tweets:
            sentiment = tweet.get('analyzed_sentiment', 'NEUTRAL')
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        print(f"Analyzed {len(analyzed_tweets)} tweets. Sentiment counts: {sentiment_counts}")
        
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
                'count': len(analyzed_tweets),
                'tweets': analyzed_tweets,
                'summary': sentiment_counts
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