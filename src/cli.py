import argparse
import pandas as pd
from src.sentiment_analyzer import analyze_sentiment
from src.visualizer import generate_visualizations
import os

def read_csv_with_encoding(file_path):
    encodings = ['utf-8', 'iso-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unable to read the file with any of the following encodings: {', '.join(encodings)}")

def process_text(text):
    try:
        return analyze_sentiment(text)
    except Exception as e:
        print(f"Error processing text: {e}")
        return {"error": str(e)}

def process_texts(texts):
    return [process_text(text) for text in texts]

def run_cli():
    parser = argparse.ArgumentParser(description='SentiTweet - Advanced Text Sentiment Analyzer')
    parser.add_argument('input_file', help='Path to the input CSV file containing texts to analyze')
    parser.add_argument('output_file', help='Path to save the output CSV file with sentiment analysis results')
    parser.add_argument('visualization_dir', help='Directory to save visualization images')
    parser.add_argument('--text_column', default='text', help='Name of the column containing the text to analyze (default: text)')
    parser.add_argument('--start_row', type=int, default=0, help='Starting row for analysis (0-indexed, inclusive)')
    parser.add_argument('--end_row', type=int, help='Ending row for analysis (0-indexed, exclusive). If not provided, will process until the end of the file')
    
    args = parser.parse_args()

    print("Loading input data...")
    try:
        input_df = read_csv_with_encoding(args.input_file)
    except ValueError as e:
        print(f"Error: {e}")
        return
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: Input file '{args.input_file}' is empty.")
        return

    if args.text_column not in input_df.columns:
        print(f"Error: Column '{args.text_column}' not found in the input file.")
        print(f"Available columns: {', '.join(input_df.columns)}")
        return

    # Select rows based on start_row and end_row
    if args.end_row is None:
        args.end_row = len(input_df)
    
    input_df = input_df.iloc[args.start_row:args.end_row]

    print(f"Processing texts from row {args.start_row} to {args.end_row-1}...")
    results = process_texts(input_df[args.text_column])
    results_df = pd.DataFrame(results)

    print("Saving results...")
    results_df.to_csv(args.output_file, index=False)
    print(f"Results saved to {args.output_file}")

    print("Generating visualizations...")
    os.makedirs(args.visualization_dir, exist_ok=True)
    generate_visualizations(results_df, args.visualization_dir)

    print("Analysis complete!")
    print(f"Visualizations saved in {args.visualization_dir}")

if __name__ == "__main__":
    run_cli()