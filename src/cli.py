import argparse
from src.data_processor import load_tweets, process_tweets, save_results
from src.visualizer import generate_visualizations

def run_cli():
    parser = argparse.ArgumentParser(description='SentiTweet - Tweet Sentiment Analyzer')
    parser.add_argument('input_file', help='Path to the input CSV file containing tweets')
    parser.add_argument('output_file', help='Path to save the output CSV file with sentiment analysis results')
    parser.add_argument('visualization_dir', help='Directory to save visualization images')
    
    args = parser.parse_args()
    
    print("Loading tweets...")
    tweets_df = load_tweets(args.input_file)
    
    print("Processing tweets...")
    results_df = process_tweets(tweets_df)
    
    print("Saving results...")
    save_results(results_df, args.output_file)
    
    print("Generating visualizations...")
    generate_visualizations(results_df, args.visualization_dir)
    
    print("Analysis complete!")