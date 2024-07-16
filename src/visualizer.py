import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def safe_plot(plot_func):
    def wrapper(*args, **kwargs):
        try:
            plot_func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {plot_func.__name__}: {str(e)}")
    return wrapper

@safe_plot
def plot_sentiment_distribution(df, output_path):
    plt.figure(figsize=(10, 6))
    df['aws_sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('AWS Sentiment Distribution')
    plt.savefig(f'{output_path}/sentiment_distribution.png')
    plt.close()
    logging.info(f"Sentiment distribution plot saved to {output_path}/sentiment_distribution.png")

@safe_plot
def plot_sentiment_comparison(df, output_path):
    plt.figure(figsize=(10, 6))
    df.groupby(['textblob_sentiment', 'aws_sentiment']).size().unstack().plot(kind='bar', stacked=True)
    plt.title('TextBlob vs AWS Sentiment Comparison')
    plt.xlabel('TextBlob Sentiment')
    plt.ylabel('Count')
    plt.legend(title='AWS Sentiment')
    plt.savefig(f'{output_path}/sentiment_comparison.png')
    plt.close()
    logging.info(f"Sentiment comparison plot saved to {output_path}/sentiment_comparison.png")

@safe_plot
def plot_sentiment_scores(df, output_path):
    scores = pd.DataFrame(df['aws_scores'].tolist(), index=df.index)
    plt.figure(figsize=(10, 6))
    scores.boxplot()
    plt.title('Distribution of AWS Sentiment Scores')
    plt.savefig(f'{output_path}/sentiment_scores.png')
    plt.close()
    logging.info(f"Sentiment scores plot saved to {output_path}/sentiment_scores.png")

@safe_plot
def plot_top_key_phrases(df, output_path):
    all_phrases = [phrase for phrases in df['key_phrases'] for phrase in phrases]
    top_phrases = Counter(all_phrases).most_common(20)
    
    plt.figure(figsize=(12, 8))
    plt.barh([phrase[0] for phrase in reversed(top_phrases)], [phrase[1] for phrase in reversed(top_phrases)])
    plt.title('Top 20 Key Phrases')
    plt.xlabel('Count')
    plt.savefig(f'{output_path}/top_key_phrases.png')
    plt.close()
    logging.info(f"Top key phrases plot saved to {output_path}/top_key_phrases.png")

@safe_plot
def plot_sentiment_by_length(df, output_path):
    df['text_length'] = df['text'].str.len()
    length_sentiment = df.groupby(pd.cut(df['text_length'], bins=5))['aws_sentiment'].value_counts(normalize=True).unstack()
    
    plt.figure(figsize=(12, 6))
    length_sentiment.plot(kind='bar', stacked=True)
    plt.title('Sentiment Distribution by Text Length')
    plt.xlabel('Text Length')
    plt.ylabel('Proportion')
    plt.legend(title='AWS Sentiment')
    plt.savefig(f'{output_path}/sentiment_by_length.png')
    plt.close()
    logging.info(f"Sentiment by length plot saved to {output_path}/sentiment_by_length.png")

def generate_visualizations(df, output_path):
    os.makedirs(output_path, exist_ok=True)
    logging.info(f"Generating visualizations in {output_path}")

    plot_sentiment_distribution(df, output_path)
    plot_sentiment_comparison(df, output_path)
    plot_sentiment_scores(df, output_path)
    plot_top_key_phrases(df, output_path)
    plot_sentiment_by_length(df, output_path)

    logging.info("Visualization generation complete")