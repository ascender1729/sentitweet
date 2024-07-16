# SentiTweet: Advanced Sentiment Analysis Tool
![SentiTweet Logo](https://github.com/ascender1729/sentitweet/blob/main/img/sentitweet_ss.jpg)

SentiTweet is a powerful sentiment analysis tool that leverages AWS Comprehend and TextBlob to analyze the sentiment of text inputs. It provides both a command-line interface and a web application for flexible usage, making it easy to understand the emotional tone of text data.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Input CSV Format](#input-csv-format)
- [Output](#output)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## Features

- **Dual Sentiment Analysis**: Utilizes both AWS Comprehend and TextBlob for comprehensive sentiment classification.
- **Multiple Input Methods**: Supports both single text analysis and batch processing of CSV files.
- **Interactive Web Dashboard**: User-friendly interface for entering text and viewing results with visualizations.
- **Command-Line Interface**: Efficient batch processing for large datasets.
- **Visualization Suite**: 
  - Sentiment distribution
  - AWS vs TextBlob sentiment comparison
  - Distribution of sentiment scores
  - Top key phrases
  - Sentiment distribution by text length
- **Entity Recognition**: Identifies and extracts key entities from the text.
- **Multi-Encoding Support**: Handles various text encodings for versatile input processing.
- **Robust Error Handling**: Comprehensive error management and logging for smooth operation.

## Tech Stack

### Backend
- **Python**: Core programming language for the application.
- **AWS Comprehend**: Cloud-based NLP service for advanced sentiment analysis.
- **TextBlob**: Python library for processing textual data.
- **pandas**: Data manipulation and analysis library.
- **matplotlib** & **seaborn**: Data visualization libraries.

### Frontend (Web Application)
- **Flask**: Lightweight WSGI web application framework.
- **HTML/CSS/JavaScript**: For the web interface.
- **Chart.js**: JavaScript library for creating interactive charts.

### Development Tools
- **pip**: Package installer for Python.
- **virtualenv**: Tool to create isolated Python environments.

## Prerequisites

- Python 3.7 or later
- AWS account with Comprehend access
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ascender1729/sentitweet.git
   cd sentitweet
   ```

2. Create and activate a virtual environment:
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
   - Configure AWS CLI with your credentials:
     ```
     aws configure
     ```

## Usage

### Web Application

1. Run the application:
   ```
   python main.py
   ```

2. Open a web browser and navigate to `http://127.0.0.1:5000`.

3. Use the interface to analyze single texts or upload CSV files for batch processing.

### Command-Line Interface

Use the following command to analyze texts from a CSV file:

```
python main.py input.csv output.csv visualizations/ --text_column text --start_row 0 --end_row 100
```

Arguments:
- `input.csv`: Path to the input CSV file containing texts to analyze
- `output.csv`: Path to save the output CSV file with sentiment analysis results
- `visualizations/`: Directory to save visualization images
- `--text_column`: Name of the column containing the text to analyze (default: 'text')
- `--start_row`: Starting row for analysis (0-indexed, inclusive, default: 0)
- `--end_row`: Ending row for analysis (0-indexed, exclusive, optional)


## Input CSV Format

The input CSV file should contain a column with the texts to be analyzed. By default, the script looks for a column named 'text', but you can specify a different column name using the `--text_column` argument.

Example input.csv:
```
id,text,date
1,"I love this product! It's amazing!",2023-01-01
2,"The service was terrible and I'm very disappointed.",2023-01-02
3,"The weather is quite nice today.",2023-01-03
```

## Output

The tool generates two types of output:

1. A CSV file containing:
   - Original text
   - AWS Comprehend sentiment
   - TextBlob sentiment
   - Sentiment scores
   - Extracted key phrases
   - Recognized entities

2. Visualization images including:
   - Sentiment distribution
   - Sentiment comparison between AWS and TextBlob
   - Distribution of sentiment scores
   - Top key phrases
   - Sentiment distribution by text length

## Error Handling

SentiTweet includes robust error handling for various scenarios:
- Invalid input file formats
- Encoding issues
- Missing columns in CSV files
- AWS Comprehend API errors

Errors are logged and reported to the user, ensuring a smooth experience even when processing large datasets.

## Contributing

Contributions to SentiTweet are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Pavan Kumar - pavankumard.pg19.ma@nitp.ac.in


Project Link: [https://github.com/ascender1729/sentitweet](https://github.com/ascender1729/sentitweet)

## Acknowledgements

- AWS Comprehend for providing powerful NLP capabilities
- TextBlob for additional sentiment analysis
- Flask for the web application framework
- Chart.js for interactive data visualizations
- The open-source community for various libraries used in this project
