import boto3
import csv
import sys
from decimal import Decimal

# ============================================
# ENTER YOUR AWS CREDENTIALS HERE
# ============================================
AWS_ACCESS_KEY_ID = 'qwertyuiopasdfghjkl'
AWS_SECRET_ACCESS_KEY = 'your own access key'
AWS_REGION = 'ap-south-1'
TABLE_NAME = 'TweetsDatabase'
# ============================================

def convert_to_dynamodb_format(value):
    """Convert values to DynamoDB compatible format"""
    if isinstance(value, float):
        return Decimal(str(value))
    elif isinstance(value, int):
        return value
    return str(value)

def import_tweets_to_dynamodb(csv_file):
    """Import tweets from CSV to DynamoDB"""
    
    print("🚀 Starting import process...")
    print(f"📁 Reading from: {csv_file}")
    print(f"📊 Target table: {TABLE_NAME}")
    print(f"🌍 Region: {AWS_REGION}\n")
    
    # Validate credentials are entered
    if AWS_ACCESS_KEY_ID == 'YOUR_ACCESS_KEY_ID_HERE' or AWS_SECRET_ACCESS_KEY == 'YOUR_SECRET_ACCESS_KEY_HERE':
        print("❌ ERROR: Please edit the script and add your AWS credentials!")
        print("\nOpen import_tweets.py in Notepad and replace:")
        print("  - YOUR_ACCESS_KEY_ID_HERE with your actual Access Key ID")
        print("  - YOUR_SECRET_ACCESS_KEY_HERE with your actual Secret Access Key")
        return
    
    # Initialize DynamoDB client with explicit credentials
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        table = dynamodb.Table(TABLE_NAME)
        
        # Test connection
        table.table_status
        print("✅ Successfully connected to DynamoDB")
        print(f"✅ Table status: Active\n")
        
    except Exception as e:
        print(f"❌ Error connecting to DynamoDB: {e}")
        print("\nTroubleshooting:")
        print("1. Verify your Access Key ID and Secret Access Key are correct")
        print("2. Check that table 'TweetsDatabase' exists in ap-south-1 region")
        print("3. Ensure your AWS account has DynamoDB permissions")
        return
    
    # Read CSV and import data
    successful_imports = 0
    failed_imports = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            print("📤 Uploading tweets to DynamoDB...")
            print("Progress: ", end='', flush=True)
            
            for index, row in enumerate(csv_reader, 1):
                try:
                    # Convert numeric fields
                    item = {
                        'tweet_id': row['tweet_id'],
                        'username': row['username'],
                        'full_name': row['full_name'],
                        'tweet_text': row['tweet_text'],
                        'timestamp': row['timestamp'],
                        'location': row['location'],
                        'comments': int(row['comments']),
                        'reshares': int(row['reshares']),
                        'likes': int(row['likes']),
                        'sentiment': row['sentiment'],
                        'category': row['category']
                    }
                    
                    # Put item into DynamoDB
                    table.put_item(Item=item)
                    successful_imports += 1
                    
                    # Progress indicator
                    if index % 500 == 0:
                        print(f"{index}...", end='', flush=True)
                    
                except Exception as e:
                    failed_imports += 1
                    if failed_imports <= 5:  # Show first 5 errors only
                        print(f"\n⚠️ Error importing tweet {row.get('tweet_id', 'unknown')}: {e}")
        
        print(f"\n\n{'='*60}")
        print("✅ IMPORT COMPLETE!")
        print(f"{'='*60}")
        print(f"✅ Successfully imported: {successful_imports} tweets")
        if failed_imports > 0:
            print(f"❌ Failed imports: {failed_imports} tweets")
        print(f"📊 Total processed: {successful_imports + failed_imports} tweets")
        print(f"\n🎉 Your DynamoDB table '{TABLE_NAME}' is ready to use!")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find file '{csv_file}'")
        print("Please make sure 'tweets_dataset.csv' is in the same folder as this script.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    # Check if CSV file exists in current directory
    csv_filename = 'tweets_dataset.csv'
    
    print("="*60)
    print("  TWEET SENTIMENT ANALYSIS - DynamoDB Import")
    print("="*60)
    print()
    

    import_tweets_to_dynamodb(csv_filename)
