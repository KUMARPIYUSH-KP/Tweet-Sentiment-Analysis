import requests
import json

# Your API Base URL
API_BASE_URL = "https://td107opk34.execute-api.ap-south-1.amazonaws.com/prod"

def test_search_endpoint():
    """Test the search endpoint"""
    print("="*60)
    print("Testing SEARCH Endpoint")
    print("="*60)
    
    # Test data
    payload = {
        "keyword": "pizza",
        "limit": 5
    }
    
    print(f"\n📤 Sending request to: {API_BASE_URL}/search")
    print(f"📋 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/search",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data.get('count', 0)} tweets")
            print("\n📊 Sample tweets:")
            
            for i, tweet in enumerate(data.get('tweets', [])[:3], 1):
                print(f"\n  Tweet {i}:")
                print(f"    Username: {tweet.get('username')}")
                print(f"    Text: {tweet.get('tweet_text')[:80]}...")
                print(f"    Sentiment: {tweet.get('sentiment')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_analyze_endpoint():
    """Test the analyze endpoint"""
    print("\n\n")
    print("="*60)
    print("Testing ANALYZE Endpoint")
    print("="*60)
    
    # Test data - sample tweets
    payload = {
        "tweets": [
            {
                "tweet_id": "test1",
                "tweet_text": "I absolutely love this product! Best purchase ever!",
                "username": "test_user1"
            },
            {
                "tweet_id": "test2",
                "tweet_text": "This is terrible. Worst experience of my life.",
                "username": "test_user2"
            },
            {
                "tweet_id": "test3",
                "tweet_text": "It's okay, nothing special.",
                "username": "test_user3"
            }
        ]
    }
    
    print(f"\n📤 Sending request to: {API_BASE_URL}/analyze")
    print(f"📋 Analyzing {len(payload['tweets'])} tweets")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analyzed {data.get('count', 0)} tweets")
            print(f"\n📊 Summary: {data.get('summary', {})}")
            
            print("\n📋 Detailed results:")
            for i, tweet in enumerate(data.get('tweets', []), 1):
                print(f"\n  Tweet {i}:")
                print(f"    Text: {tweet.get('tweet_text')[:60]}...")
                print(f"    Sentiment: {tweet.get('analyzed_sentiment')}")
                scores = tweet.get('sentiment_scores', {})
                print(f"    Scores: Pos:{scores.get('positive'):.2f} Neg:{scores.get('negative'):.2f} Neu:{scores.get('neutral'):.2f}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    print("\n🚀 AWS Tweet Sentiment Analysis - API Testing")
    print("="*60)
    print(f"API Base URL: {API_BASE_URL}")
    print("="*60)
    
    # Test both endpoints
    test_search_endpoint()
    test_analyze_endpoint()
    
    print("\n\n" + "="*60)
    print("✅ Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    # First check if requests library is installed
    try:
        import requests
    except ImportError:
        print("Installing requests library...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'requests'])
        import requests
    
    main()