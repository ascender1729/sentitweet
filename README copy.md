# SentiTweet: Advanced Sentiment Analysis Dashboard

SentiTweet is an advanced sentiment analysis tool that uses AWS Comprehend and TextBlob to analyze the sentiment of text inputs. It provides a user-friendly web interface for inputting text and visualizing the sentiment analysis results.

## Features

- Sentiment analysis using AWS Comprehend and TextBlob
- Interactive web dashboard
- Visualization of sentiment scores and comparisons
- Key phrase extraction and entity recognition
- Dark mode toggle
- Ability to save analysis results

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sentitweet.git
   cd sentitweet
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your AWS credentials:
   - Create an AWS account if you don't have one
   - Set up AWS CLI and configure it with your credentials

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. Open a web browser and go to `http://127.0.0.1:5000/`

3. Enter your text in the input box and click "Analyze"

4. View the sentiment analysis results and visualizations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.