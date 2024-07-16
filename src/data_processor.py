import pandas as pd
from src.sentiment_analyzer import analyze_sentiment

def load_tweets(file_path):
    return pd.read_csv(file_path)

def process_tweets(tweets_df):
    results = []
    for _, row in tweets_df.iterrows():
        result = analyze_sentiment(row['text'])
        results.append(result)
    return pd.DataFrame(results)

def save_results(results_df, output_path):
    results_df.to_csv(output_path, index=False)