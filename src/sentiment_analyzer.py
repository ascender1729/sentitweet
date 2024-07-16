import boto3
from textblob import TextBlob
import re

def clean_tweet(tweet):
    return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_textblob_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'POSITIVE'
    elif analysis.sentiment.polarity < 0:
        return 'NEGATIVE'
    else:
        return 'NEUTRAL'

def analyze_sentiment(tweet):
    comprehend = boto3.client('comprehend')
    
    aws_response = comprehend.detect_sentiment(Text=tweet, LanguageCode='en')
    key_phrases = comprehend.detect_key_phrases(Text=tweet, LanguageCode='en')
    entities = comprehend.detect_entities(Text=tweet, LanguageCode='en')
    
    textblob_sentiment = get_textblob_sentiment(tweet)
    
    return {
        'text': tweet,
        'aws_sentiment': aws_response['Sentiment'],
        'aws_scores': aws_response['SentimentScore'],
        'textblob_sentiment': textblob_sentiment,
        'key_phrases': [phrase['Text'] for phrase in key_phrases['KeyPhrases']],
        'entities': [{'Text': entity['Text'], 'Type': entity['Type']} for entity in entities['Entities']],
        'word_count': len(tweet.split()),
        'char_count': len(tweet)
    }