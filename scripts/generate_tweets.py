import csv
import random
from datetime import datetime, timedelta
import uuid

# Tweet templates by category and sentiment
tweet_templates = {
    'tech': {
        'positive': [
            "Just upgraded to the new {product}! The performance is incredible 🚀",
            "Finally got my hands on {product}. Worth every penny!",
            "The {product} launch event was amazing! Can't wait to try it out",
            "Loving the new features in {product}. Game changer!",
            "{product} is revolutionizing how we work. Highly recommend!"
        ],
        'negative': [
            "Disappointed with {product}. Expected much better quality",
            "The new {product} update broke everything. So frustrated!",
            "{product} customer service is terrible. Been waiting for days",
            "Regret buying {product}. Complete waste of money",
            "Why is {product} so expensive for such poor performance?"
        ],
        'neutral': [
            "Checking out the specs for {product}. Anyone have experience with it?",
            "Thinking about getting {product}. What do you all think?",
            "New {product} announcement today. Here are the details:",
            "Comparing {product} with alternatives. Still undecided",
            "{product} is now available in stores. Price starts at $999"
        ]
    },
    'sports': {
        'positive': [
            "What a game! {team} absolutely dominated tonight! 🏆",
            "{player} is on fire this season! MVP material for sure",
            "Best match I've seen in years! {team} fought till the end",
            "Incredible performance by {player}! Pure talent 💪",
            "{team} winning streak continues! Championship bound!"
        ],
        'negative': [
            "Terrible performance by {team} today. So disappointing",
            "{player} needs to step up. This is unacceptable",
            "Another loss for {team}. When will this end?",
            "Worst game of the season. {team} looked completely lost",
            "Can't believe {player} missed that. Cost us the game!"
        ],
        'neutral': [
            "{team} vs {team} tonight at 8 PM. Who are you rooting for?",
            "{player} stats this season: 25 PPG, 8 RPG, 6 APG",
            "Game update: {team} leading 45-42 at halftime",
            "Breaking: {player} traded to {team}. Thoughts?",
            "{team} announces new coach for next season"
        ]
    },
    'entertainment': {
        'positive': [
            "Just finished watching {movie}. Absolutely loved it! ⭐⭐⭐⭐⭐",
            "{movie} is a masterpiece! Everyone needs to see this",
            "Can't stop listening to {song}. On repeat all day!",
            "{artist} new album is pure gold. Best release this year!",
            "Finally saw {movie}. Worth all the hype and more!"
        ],
        'negative': [
            "{movie} was such a letdown. Don't waste your time",
            "Disappointed with {artist} new album. Expected better",
            "Two hours of my life I'll never get back. {movie} was terrible",
            "{song} is overhyped. Don't understand the popularity",
            "Walked out of {movie}. Couldn't take it anymore"
        ],
        'neutral': [
            "{movie} releases this Friday. Planning to watch?",
            "Currently watching {movie}. 30 minutes in so far",
            "{artist} announces world tour dates. Tickets on sale Monday",
            "Poll: Best {movie} character? Cast your vote below",
            "{song} now available on all streaming platforms"
        ]
    },
    'food': {
        'positive': [
            "Just tried {restaurant}! Best {dish} I've ever had 😋",
            "Homemade {dish} turned out perfect! Recipe in comments",
            "{restaurant} never disappoints. Always amazing food",
            "This {dish} is absolutely delicious! Highly recommend",
            "Found my new favorite spot! {restaurant} is incredible"
        ],
        'negative': [
            "Terrible experience at {restaurant}. Food was cold",
            "Tried making {dish} and it was a disaster 😭",
            "{restaurant} quality has really gone downhill",
            "Overpriced and underwhelming. {restaurant} was disappointing",
            "Food poisoning from {restaurant}. Never going back!"
        ],
        'neutral': [
            "Anyone tried the new {restaurant} downtown?",
            "Looking for good {dish} recommendations in the area",
            "{restaurant} has a new menu. Checking it out tomorrow",
            "What's your go-to order at {restaurant}?",
            "Craving {dish} today. Where should I go?"
        ]
    },
    'daily': {
        'positive': [
            "Beautiful morning! Ready to tackle the day ☀️",
            "Finally Friday! Best day of the week!",
            "Had the most productive day today! Feeling accomplished",
            "Nothing beats a lazy Sunday morning with coffee ☕",
            "Great day with family and friends. Feeling blessed!"
        ],
        'negative': [
            "Mondays are the worst. Can't wait for the weekend",
            "Traffic is absolutely terrible today. Running late again",
            "Stuck in a boring meeting for 3 hours. Send help!",
            "Worst day ever. Everything that could go wrong did",
            "Can't believe I have to work on a Saturday. So unfair!"
        ],
        'neutral': [
            "Another day, another dollar. Off to work I go",
            "Weather forecast says rain all week",
            "Anyone else working from home today?",
            "Coffee run before the morning meeting",
            "Halfway through the week already. Time flies"
        ]
    },
    'politics': {
        'positive': [
            "Finally some good news! New policy will help millions",
            "Proud of our city for taking action on climate change",
            "Historic vote today! Democracy in action 🗳️",
            "Great speech by the mayor today. Inspiring leadership",
            "Community coming together for positive change!"
        ],
        'negative': [
            "This new policy makes no sense. Completely disappointed",
            "Our leaders need to do better. This is unacceptable",
            "Broken promises again. When will things change?",
            "The budget cuts are going to hurt working families",
            "Can't believe they passed this bill. Huge mistake"
        ],
        'neutral': [
            "City council meeting scheduled for next Tuesday at 6 PM",
            "New policy proposal announced. Details here:",
            "Election results: 52% voter turnout this year",
            "Public hearing on proposed changes next week",
            "Poll: What's your take on the new infrastructure plan?"
        ]
    }
}

# Data for randomization
products = ['iPhone 15', 'Samsung Galaxy', 'MacBook Pro', 'PS5', 'Tesla Model 3', 'iPad Pro', 'AirPods Pro']
teams = ['Lakers', 'Warriors', 'Heat', 'Celtics', 'Yankees', 'Red Sox', 'Manchester United', 'Real Madrid']
players = ['LeBron James', 'Stephen Curry', 'Messi', 'Ronaldo', 'Virat Kohli', 'Tom Brady']
movies = ['Oppenheimer', 'Barbie', 'Dune', 'The Matrix', 'Inception', 'Avatar']
songs = ['Anti-Hero', 'Flowers', 'Blinding Lights', 'As It Was']
artists = ['Taylor Swift', 'The Weeknd', 'Ed Sheeran', 'Beyonce', 'Drake']
restaurants = ["Joe's Pizza", 'Olive Garden', 'Chipotle', 'Starbucks', 'Thai Express', 'Burger King']
dishes = ['pizza', 'pasta', 'sushi', 'tacos', 'biryani', 'ramen', 'burger']

cities = ['Mumbai', 'Delhi', 'Bangalore', 'New York', 'London', 'Tokyo', 'Singapore', 'Dubai', 'Sydney', 'Toronto']

first_names = ['Raj', 'Priya', 'Amit', 'Sneha', 'Rahul', 'Anjali', 'Vikram', 'Pooja', 'Arjun', 'Kavya',
               'John', 'Sarah', 'Mike', 'Emily', 'David', 'Lisa', 'Alex', 'Emma', 'Chris', 'Sophia']
last_names = ['Sharma', 'Kumar', 'Patel', 'Singh', 'Gupta', 'Reddy', 'Shah', 'Verma', 'Mehta', 'Khan',
              'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Wilson', 'Taylor']

def generate_username(first, last):
    patterns = [
        f"{first.lower()}{last.lower()}",
        f"{first.lower()}_{last.lower()}",
        f"{first.lower()}{random.randint(10, 99)}",
        f"{last.lower()}{first[0].lower()}{random.randint(100, 999)}",
        f"{first.lower()}.{last.lower()}",
    ]
    return random.choice(patterns)

def generate_tweet(category, sentiment):
    template = random.choice(tweet_templates[category][sentiment])
    
    # Replace placeholders
    replacements = {
        '{product}': random.choice(products),
        '{team}': random.choice(teams),
        '{player}': random.choice(players),
        '{movie}': random.choice(movies),
        '{song}': random.choice(songs),
        '{artist}': random.choice(artists),
        '{restaurant}': random.choice(restaurants),
        '{dish}': random.choice(dishes)
    }
    
    for key, value in replacements.items():
        template = template.replace(key, value)
    
    return template

def generate_tweets(num_tweets=10000):
    tweets = []
    categories = list(tweet_templates.keys())
    sentiments = ['positive', 'negative', 'neutral']
    
    # Distribution: 40% positive, 30% negative, 30% neutral
    sentiment_distribution = ['positive'] * 4000 + ['negative'] * 3000 + ['neutral'] * 3000
    random.shuffle(sentiment_distribution)
    
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(num_tweets):
        category = random.choice(categories)
        sentiment = sentiment_distribution[i]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        username = generate_username(first_name, last_name)
        
        tweet_text = generate_tweet(category, sentiment)
        tweet_id = str(uuid.uuid4())[:8]
        
        # Random timestamp within last 30 days
        random_seconds = random.randint(0, 30 * 24 * 60 * 60)
        timestamp = start_date + timedelta(seconds=random_seconds)
        
        # Engagement metrics (more engagement for positive tweets)
        if sentiment == 'positive':
            comments = random.randint(5, 150)
            reshares = random.randint(10, 300)
            likes = random.randint(50, 1000)
        elif sentiment == 'negative':
            comments = random.randint(2, 80)
            reshares = random.randint(1, 50)
            likes = random.randint(5, 200)
        else:
            comments = random.randint(1, 40)
            reshares = random.randint(1, 30)
            likes = random.randint(10, 150)
        
        tweet = {
            'tweet_id': tweet_id,
            'username': username,
            'full_name': f"{first_name} {last_name}",
            'tweet_text': tweet_text,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'location': random.choice(cities),
            'comments': comments,
            'reshares': reshares,
            'likes': likes,
            'sentiment': sentiment,
            'category': category
        }
        
        tweets.append(tweet)
    
    return tweets

def save_to_csv(tweets, filename='tweets_dataset.csv'):
    fieldnames = ['tweet_id', 'username', 'full_name', 'tweet_text', 'timestamp', 
                  'location', 'comments', 'reshares', 'likes', 'sentiment', 'category']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tweets)
    
    print(f"✅ Successfully generated {len(tweets)} tweets!")
    print(f"📁 Saved to: {filename}")
    print(f"\nDataset Statistics:")
    print(f"  Positive tweets: {sum(1 for t in tweets if t['sentiment'] == 'positive')}")
    print(f"  Negative tweets: {sum(1 for t in tweets if t['sentiment'] == 'negative')}")
    print(f"  Neutral tweets: {sum(1 for t in tweets if t['sentiment'] == 'neutral')}")

if __name__ == "__main__":
    print("🚀 Generating 10,000 realistic tweets...")
    tweets = generate_tweets(10000)
    save_to_csv(tweets)
    print("\n✅ Dataset ready for AWS import!")