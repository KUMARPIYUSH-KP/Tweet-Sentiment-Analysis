import csv
import random
from datetime import datetime, timedelta
import uuid
import boto3

# Initialize DynamoDB - REPLACE WITH YOUR CREDENTIALS
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-south-1',
    aws_access_key_id='you have to enter your own',  # ⚠️ REPLACE THIS
    aws_secret_access_key='you have to enter your own key'  # ⚠️ REPLACE THIS
)
table = dynamodb.Table('TweetsDatabase')

# Comprehensive tweet templates for ALL categories
tweet_templates = {
    'ai_ml': {
        'positive': [
            "ChatGPT just helped me write amazing code! AI is revolutionizing development 🤖",
            "Machine Learning model achieved 98% accuracy! AI technology is incredible",
            "Artificial Intelligence is transforming healthcare. Lives are being saved!",
            "Just deployed my first AI chatbot! Machine learning is so powerful",
            "Deep learning breakthrough! AI can now detect diseases earlier than doctors",
            "OpenAI released new features! Artificial intelligence keeps getting better",
            "My AI assistant increased productivity by 300%! Game changer",
            "Neural networks are amazing! Just trained my first AI model",
            "Generative AI tools like Midjourney creating stunning art! Future is here",
            "AI automation saved our company 50 hours/week! Incredible technology"
        ],
        'negative': [
            "AI is taking jobs away. Worried about artificial intelligence replacing workers",
            "Machine learning bias is a serious problem. AI ethics need attention",
            "ChatGPT gave me wrong information. AI still has limitations",
            "Deepfakes are dangerous. Artificial intelligence misuse is scary",
            "AI surveillance concerns. Privacy is dead with machine learning everywhere"
        ],
        'neutral': [
            "New AI course starting next month. Machine learning fundamentals",
            "Google launches new artificial intelligence research lab in India",
            "AI market expected to reach $500B by 2025. Machine learning growth",
            "Python vs R for machine learning? Which AI tool is better?",
            "Artificial intelligence job openings up 40%. AI careers booming"
        ]
    },
    
    'sports': {
        'positive': [
            "India won the cricket World Cup! Historic victory! 🏏🇮🇳",
            "IPL final was absolutely thrilling! Best cricket match ever!",
            "Virat Kohli century! Indian cricket team dominates again!",
            "FIFA World Cup finals! Football at its finest! ⚽",
            "Olympics gold medal! India's best sports performance!",
            "Champions League match was epic! Football fans celebrate!",
            "Tennis Grand Slam! Sports history made today!",
            "NBA finals game 7! Basketball excitement at peak!",
            "Premier League title decided! Football season climax!",
            "Kabaddi Pro League finals! Indian sports growing globally!"
        ],
        'negative': [
            "India lost cricket match. Disappointing sports performance",
            "Football match was boring. Poor sports entertainment",
            "Cricket management needs reform. Sports administration failing",
            "IPL spot-fixing scandal. Sports integrity questioned",
            "Injury ruins player's career. Sad day for sports"
        ],
        'neutral': [
            "Cricket schedule released. India vs Pakistan next month",
            "Football transfer news: Ronaldo joins new club for $200M",
            "Sports betting legalized in 5 new states",
            "Olympics venue construction 60% complete. Sports infrastructure",
            "Cricket World Cup 2025 host announced. Sports event planning"
        ]
    },
    
    'content_creation': {
        'positive': [
            "Just hit 100K subscribers on YouTube! Content creation journey paying off!",
            "Instagram Reels went viral! 5M views in 24 hours! Content creator life 🎥",
            "LinkedIn post got 50K impressions! Content marketing works!",
            "My blog reached 1M monthly visitors! Content writing success!",
            "TikTok video trending #1! Social media content creation is amazing",
            "Podcast crossed 10K downloads! Audio content resonates with people",
            "Twitter thread got 100K likes! Content curation strategy works",
            "Started making $5K/month from content! Creator economy is real",
            "YouTube monetization approved! Content creator dreams coming true",
            "Collaboration with major brand! Content creation opens doors"
        ],
        'negative': [
            "Content creation burnout is real. Struggling to post daily",
            "Algorithm changes killed my reach. Content visibility down 70%",
            "Copyright strike on my video. Content creator struggles",
            "Only 10 views after 6 hours. Content creation is tough",
            "Negative comments affecting mental health. Content creator life hard"
        ],
        'neutral': [
            "Best content creation tools for 2025? Looking for recommendations",
            "Content calendar template released. Planning 30 days ahead",
            "YouTube announces new monetization policies. Content creators affected",
            "Instagram vs TikTok for content? Which platform is better?",
            "Content creation course launching next month. Registration open"
        ]
    },
    
    'it_jobs': {
        'positive': [
            "Got offer from Google! Software Engineer role! 45 LPA package! 🎉",
            "Microsoft hiring 1000 developers in India! IT jobs boom!",
            "Just got promoted to Senior Developer! IT career growth is amazing",
            "Switched to Amazon! Cloud Engineer role with 60% salary hike!",
            "Remote IT job lets me work from anywhere! Tech career flexibility",
            "Startup offered me CTO position! IT opportunities are incredible",
            "Full-stack developer demand at all-time high! IT sector thriving",
            "DevOps salary crossed 25 LPA! IT jobs paying well",
            "Data Science job offers from 5 companies! Tech skills valuable",
            "Cybersecurity roles in high demand! IT security jobs paying 30+ LPA"
        ],
        'negative': [
            "IT layoffs at major tech companies. Job security concerns",
            "Coding interview rejected again. IT job market is tough",
            "IT company forcing return to office. Remote work ending",
            "Toxic work culture in IT. 80 hour weeks not sustainable",
            "Freshers struggling to find IT jobs. Tech hiring freeze"
        ],
        'neutral': [
            "Infosys hiring 10,000 freshers. IT job opportunities for graduates",
            "TCS salary hike announcement next month. IT compensation review",
            "Top IT skills for 2025: Python, AWS, React, DevOps",
            "IT job market analysis: Demand vs supply in tech sector",
            "Wipro work from home policy update. IT companies hybrid model"
        ]
    },
    
    'non_it_jobs': {
        'positive': [
            "Got selected for Civil Services! IAS dream achieved! 🇮🇳",
            "Chartered Accountant exam cleared! CA career starts now!",
            "Teaching job at top university! Education sector opportunity",
            "Selected for MBA at IIM Ahmedabad! Management career path",
            "Marketing Manager role at Unilever! FMCG career growth",
            "Mechanical Engineer position at Tata Motors! Core engineering job",
            "Got Doctor job at AIIMS! Medical profession pride",
            "Bank PO exam cleared! Banking sector career secured",
            "Fashion Designer showcase at Lakmé! Creative career success",
            "Journalist position at Times of India! Media industry job"
        ],
        'negative': [
            "Non-IT salaries much lower than tech. Pay disparity is real",
            "Teaching job pay is inadequate. Education sector underpaid",
            "Manufacturing job losses continue. Core sector struggling",
            "Retail jobs being automated. Non-IT career concerns",
            "Agriculture income declining. Farming jobs not sustainable"
        ],
        'neutral': [
            "RBI recruits 1000 officers. Banking jobs notification out",
            "UPSC notification 2025. Civil services exam dates announced",
            "MBA placements average 18 LPA. Management jobs market",
            "Healthcare workers in demand. Medical jobs growing 15%",
            "Teaching jobs: 5000 positions in Delhi schools"
        ]
    },
    
    'govt_jobs': {
        'positive': [
            "SSC CGL result out! Selected for government job! Finally! 🎊",
            "Railway recruitment: Got Ticket Collector post! Govt job secured",
            "UPSC CSE cleared! IAS officer journey begins! Dream come true!",
            "Bank PO interview cleared! SBI job confirmed! Govt sector stable",
            "Defence job selected! Indian Army proud moment! 🇮🇳",
            "ISRO scientist position! Government research job amazing!",
            "High Court Clerk exam cleared! Judicial govt job secured",
            "Police SI recruitment success! Law enforcement career starts",
            "PSU job at BHEL! Government enterprise career stable",
            "Post Office Postman selection! Govt job with pension benefits"
        ],
        'negative': [
            "Govt job exam postponed again. Recruitment delays frustrating",
            "Government job vacancies not filled for 5 years. System broken",
            "Govt salary increment pending. Public sector pay issues",
            "Age limit exclusion unfair. Government jobs accessibility problem",
            "Govt exam paper leaked. Recruitment integrity questioned"
        ],
        'neutral': [
            "UPSC notification 2025: 1000 IAS/IPS posts. Government jobs",
            "Railway RRB recruitment 35,000 posts announced. Govt sector hiring",
            "SSC exam calendar 2025 released. Government job schedule",
            "PSU recruitment through GATE scores. Public sector jobs",
            "Defence recruitment rally schedule. Military govt jobs dates"
        ]
    },
    
    'pvt_jobs': {
        'positive': [
            "Joined Reliance as Manager! Private sector salary 18 LPA!",
            "Got job at Tata Group! Private company career growth excellent",
            "HDFC Bank hired me! Private banking job with perks",
            "Flipkart offered Supply Chain role! E-commerce job exciting",
            "Private firm work culture is amazing! Flexibility and growth",
            "Startup gave me ESOP worth 50 lakhs! Private sector benefits",
            "Pharmaceutical company job with global exposure! MNC career",
            "Private consultancy role in Big 4! Professional services job",
            "Media company creative director role! Private sector opportunity",
            "Automobile industry private job! Engineering MNC career"
        ],
        'negative': [
            "Private sector layoffs brutal. No job security in companies",
            "Work-life balance zero in private jobs. 12 hour days normal",
            "Private company fired without notice. Corporate culture toxic",
            "Salary delayed 2 months in private firm. Financial stress",
            "Private sector exploitation. No employee rights protection"
        ],
        'neutral': [
            "Private vs government jobs comparison. Which is better?",
            "Private company hiring trends 2025. Job market analysis",
            "Salary negotiation tips for private sector. Career advice",
            "Top private employers in India. Job opportunities ranking",
            "Private sector job growth 8% this year. Employment data"
        ]
    },
    
    'news': {
        'positive': [
            "India GDP growth strongest in world! Economic news positive 📈",
            "New education policy approved! Reforms will help millions",
            "Cancer cure breakthrough announced! Medical news gives hope",
            "Solar energy adoption soars! Environmental news encouraging",
            "Women's safety laws strengthened! Social progress news",
            "Digital India initiative success! Technology penetration high",
            "Infrastructure development accelerates! Roads and railways boost",
            "Poverty reduced by 15%! Social welfare news positive",
            "India's space mission success! ISRO achievements celebrated",
            "Startup ecosystem funding record high! Business news upbeat"
        ],
        'negative': [
            "Inflation hits 8%! Economic news concerning for middle class",
            "Unemployment rate increases. Job market news worrying",
            "Air pollution at dangerous levels! Environmental crisis news",
            "Crime rates rising in cities. Law and order news alarming",
            "Healthcare system overwhelmed. Medical infrastructure news bad",
            "Corruption scandal exposed! Political news disappointing",
            "Natural disaster kills hundreds. Tragedy news devastating",
            "Stock market crash! Financial news causes panic",
            "Terrorist attack in border area. Security news concerning",
            "Drought affects farmers badly. Agricultural news distressing"
        ],
        'neutral': [
            "Budget 2025 announced. Tax changes and allocations detailed",
            "Election schedule released. Voting dates across states",
            "Supreme Court verdict on landmark case today",
            "RBI monetary policy meeting. Interest rate decision awaited",
            "Census data collection begins nationwide. Demographics news",
            "International summit hosted by India. Diplomatic news",
            "Weather forecast: Heavy rains expected. Monsoon update",
            "Sports tournament schedule announced. Events calendar",
            "New metro line inauguration tomorrow. Infrastructure news",
            "Festival holidays declared. Public holiday announcement"
        ]
    },
    
    'study': {
        'positive': [
            "Scored 98% in board exams! Hard work pays off! 📚",
            "JEE Advanced rank under 100! IIT dreams coming true!",
            "NEET cleared with AIR 50! Medical college admission confirmed!",
            "Study group method worked! Semester topper achieved!",
            "Scholarship worth 10 lakhs received! Education funding secured!",
            "CAT 99.9 percentile! IIM admission guaranteed!",
            "Got admission in MIT! International study dream realized!",
            "Research paper published! Academic achievement proud moment!",
            "Won National Science Olympiad! Student competition success!",
            "PhD scholarship from Cambridge! Higher education opportunity!"
        ],
        'negative': [
            "Failed entrance exam. Study pressure is overwhelming",
            "Can't afford college fees. Education cost burden huge",
            "Exam stress causing health issues. Student mental health crisis",
            "Study material quality poor. Education system needs reform",
            "Dropped out due to financial issues. Educational dreams shattered"
        ],
        'neutral': [
            "CBSE board exam date sheet released. Study schedule planning",
            "Top 10 engineering colleges in India 2025. Education rankings",
            "Study abroad opportunities: Scholarships available for students",
            "Online vs offline classes debate. Education delivery methods",
            "Best study techniques for competitive exams. Tips and tricks"
        ]
    },
    
    'competitions': {
        'positive': [
            "Won National Hackathon! 5 lakh prize money! Competition success! 💻",
            "Coding competition first place! Google Code Jam victory!",
            "Business plan competition winner! Startup funding secured!",
            "Quiz competition champion! Knowledge competition triumph!",
            "Science fair gold medal! Student competition achievement!",
            "Debate competition winner at state level! Oratory skills win!",
            "Sports competition medal! Athletic achievement celebrated!",
            "Art competition grand prize! Creative talent recognized!",
            "Photography contest winner! Skill competition success!",
            "Dance competition trophy! Performance art competition win!"
        ],
        'negative': [
            "Lost competition in finals. Came so close to winning",
            "Competition judging was biased. Unfair evaluation process",
            "Disqualified from competition on technicality. Rules unclear",
            "Competition stress caused burnout. Pressure too high",
            "Couldn't participate due to lack of resources. Inequality"
        ],
        'neutral': [
            "Hackathon registration open. Competition starts next month",
            "Top 10 coding competitions in India. Contest calendar 2025",
            "Quiz competition rules and format. Contest preparation guide",
            "Business competition judging criteria released. Evaluation matrix",
            "Competition prize money distribution: 15 lakhs total pool"
        ]
    }
}

# Enhanced data lists
companies = ['Google', 'Microsoft', 'Amazon', 'TCS', 'Infosys', 'Wipro', 'HCL', 'Cognizant', 
            'Accenture', 'IBM', 'Flipkart', 'Paytm', 'Zomato', 'Swiggy', 'Reliance', 
            'Tata', 'Mahindra', 'Bharti Airtel', 'HDFC Bank', 'ICICI']

cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 
         'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Indore', 'Nagpur', 'Kochi']

first_names = ['Raj', 'Priya', 'Amit', 'Sneha', 'Rahul', 'Anjali', 'Vikram', 'Pooja', 
              'Arjun', 'Kavya', 'Rohan', 'Meera', 'Aditya', 'Neha', 'Karan', 'Isha',
              'Siddharth', 'Ananya', 'Harsh', 'Sakshi']

last_names = ['Sharma', 'Kumar', 'Patel', 'Singh', 'Gupta', 'Reddy', 'Shah', 'Verma', 
             'Mehta', 'Khan', 'Joshi', 'Nair', 'Desai', 'Malhotra', 'Kapoor', 'Bansal',
             'Agarwal', 'Rao', 'Iyer', 'Chopra']

def generate_username(first, last):
    patterns = [
        f"{first.lower()}{last.lower()}",
        f"{first.lower()}_{last.lower()}",
        f"{first.lower()}{random.randint(10, 99)}",
        f"{last.lower()}{first[0].lower()}{random.randint(100, 999)}",
        f"{first.lower()}.{last.lower()}",
    ]
    return random.choice(patterns)

def generate_comprehensive_tweet(category):
    """Generate a tweet for the specified category"""
    sentiment = random.choice(['positive', 'negative', 'neutral'])
    
    # Weight towards positive (40%), negative (30%), neutral (30%)
    weights = [0.4, 0.3, 0.3]
    sentiment = random.choices(['positive', 'negative', 'neutral'], weights=weights)[0]
    
    template = random.choice(tweet_templates[category][sentiment])
    
    # Replace placeholders if any
    template = template.replace('{company}', random.choice(companies))
    
    return template, sentiment

def add_comprehensive_tweets():
    """Add tweets for ALL categories"""
    
    print("="*70)
    print("  COMPREHENSIVE TWEET GENERATION - ALL CATEGORIES")
    print("="*70)
    print()
    
    # Define how many tweets per category
    category_distribution = {
        'ai_ml': 1000,
        'sports': 1500,
        'content_creation': 800,
        'it_jobs': 1200,
        'non_it_jobs': 800,
        'govt_jobs': 1000,
        'pvt_jobs': 800,
        'news': 1500,
        'study': 1000,
        'competitions': 600
    }
    
    total_tweets = sum(category_distribution.values())
    print(f"📊 Will generate {total_tweets} tweets across {len(category_distribution)} categories\n")
    
    start_date = datetime.now() - timedelta(days=60)  # Last 60 days
    total_added = 0
    total_failed = 0
    
    for category, count in category_distribution.items():
        print(f"\n{'='*70}")
        print(f"📝 Generating {count} tweets for category: {category.upper().replace('_', ' ')}")
        print(f"{'='*70}")
        
        added = 0
        failed = 0
        
        for i in range(count):
            try:
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                username = generate_username(first_name, last_name)
                
                tweet_text, sentiment = generate_comprehensive_tweet(category)
                tweet_id = str(uuid.uuid4())[:8]
                
                # Random timestamp within last 60 days
                random_seconds = random.randint(0, 60 * 24 * 60 * 60)
                timestamp = start_date + timedelta(seconds=random_seconds)
                
                # Engagement metrics based on sentiment
                if sentiment == 'positive':
                    comments = random.randint(10, 200)
                    reshares = random.randint(20, 400)
                    likes = random.randint(100, 2000)
                elif sentiment == 'negative':
                    comments = random.randint(5, 100)
                    reshares = random.randint(2, 80)
                    likes = random.randint(10, 300)
                else:
                    comments = random.randint(2, 60)
                    reshares = random.randint(1, 50)
                    likes = random.randint(20, 200)
                
                item = {
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
                
                # Add to DynamoDB
                table.put_item(Item=item)
                added += 1
                total_added += 1
                
                if (i + 1) % 100 == 0:
                    print(f"  ✅ Progress: {i + 1}/{count} tweets added...")
                    
            except Exception as e:
                failed += 1
                total_failed += 1
                if failed <= 3:  # Show first 3 errors only
                    print(f"  ❌ Error: {e}")
        
        print(f"  ✅ Category '{category}' complete: {added} tweets added")
    
    print(f"\n\n{'='*70}")
    print(f"  🎉 GENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f"  ✅ Total tweets added: {total_added}")
    print(f"  ❌ Total failed: {total_failed}")
    print(f"  📊 Success rate: {(total_added/(total_added+total_failed)*100):.1f}%")
    print(f"{'='*70}")
    print(f"\n  📈 Your database now has approximately {10000 + total_added} tweets!")
    print(f"\n  🔍 You can now search for:")
    print(f"     • AI, machine learning, ChatGPT, artificial intelligence")
    print(f"     • Cricket, sports, football, IPL, Olympics")
    print(f"     • Content, YouTube, Instagram, creator, viral")
    print(f"     • IT jobs, software engineer, developer, Google")
    print(f"     • Government jobs, SSC, UPSC, railway, bank")
    print(f"     • Private jobs, Tata, Reliance, startup")
    print(f"     • News, politics, economy, breaking")
    print(f"     • Study, exam, JEE, NEET, scholarship")
    print(f"     • Competition, hackathon, contest, winner")
    print(f"     • And many more keywords!")
    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: Make sure you've added your AWS credentials in the script!\n")
    
    response = input("Do you want to proceed? This will add ~10,000 new tweets to your database. (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        print("\n🚀 Starting tweet generation...\n")
        add_comprehensive_tweets()
        print("\n✅ All done! Refresh your website and start searching!\n")
    else:
        print("\n❌ Operation cancelled.\n")