from flask import Flask, request, render_template_string, jsonify, send_file
from src.sentiment_analyzer import analyze_sentiment
import pandas as pd
import logging
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and file.filename.endswith('.csv'):
            try:
                # Try UTF-8 first
                df = pd.read_csv(file)
            except UnicodeDecodeError:
                # If UTF-8 fails, try other encodings
                try:
                    file.seek(0)  # Reset file pointer
                    df = pd.read_csv(file, encoding='iso-8859-1')
                except Exception as e:
                    return f"Error reading the CSV file: {str(e)}"
            
            start_row = int(request.form.get('start_row', 0))
            end_row = int(request.form.get('end_row', len(df)))
            text_column = request.form.get('text_column', 'text')
            
            if text_column not in df.columns:
                return f"Column '{text_column}' not found in the CSV file. Available columns are: {', '.join(df.columns)}"
            
            df = df.iloc[start_row:end_row]
            results = []
            for text in df[text_column]:
                try:
                    result = analyze_sentiment(text)
                    results.append(result)
                except Exception as e:
                    app.logger.error(f"Error analyzing text: {text}. Error: {str(e)}")
                    results.append({"error": str(e)})
            
            results_df = pd.DataFrame(results)
            
            # Generate visualizations
            try:
                visualizations = generate_visualizations(results_df)
            except Exception as e:
                app.logger.error(f"Error generating visualizations: {str(e)}")
                visualizations = {}
            
            return render_results(results_df, visualizations)
    
    return render_template_string(''' 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SentiTweet Advanced Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
        <style>
            body { 
                background-color: #f0f2f5; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .dashboard-card {
                background-color: #ffffff;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                overflow: hidden;
            }
            .dashboard-card:hover { 
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            }
            .card-header {
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
                padding: 15px;
                border-bottom: none;
            }
            .card-body {
                padding: 20px;
            }
            .scroll-box {
                max-height: 200px;
                overflow-y: auto;
                scrollbar-width: thin;
                scrollbar-color: #4a90e2 #f0f2f5;
            }
            .scroll-box::-webkit-scrollbar {
                width: 8px;
            }
            .scroll-box::-webkit-scrollbar-track {
                background: #f0f2f5;
            }
            .scroll-box::-webkit-scrollbar-thumb {
                background-color: #4a90e2;
                border-radius: 20px;
            }
            #tweet-form, #csv-form {
                background-color: #ffffff;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 30px;
            }
            .btn-primary {
                background-color: #4a90e2;
                border-color: #4a90e2;
                padding: 10px 20px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            .btn-primary:hover {
                background-color: #3a7ac8;
                border-color: #3a7ac8;
                transform: translateY(-2px);
            }
            .animate-pop {
                animation: pop 0.3s ease-in-out;
            }
            @keyframes pop {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            #tweet-input {
                min-height: 100px;
                resize: vertical;
            }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-dark bg-primary">
            <div class="container">
                <span class="navbar-brand mb-0 h1">SentiTweet Advanced Dashboard</span>
            </div>
        </nav>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <ul class="nav nav-tabs" id="myTab" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active" id="single-tab" data-bs-toggle="tab" data-bs-target="#single" type="button" role="tab" aria-controls="single" aria-selected="true">Single Text Analysis</button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="csv-tab" data-bs-toggle="tab" data-bs-target="#csv" type="button" role="tab" aria-controls="csv" aria-selected="false">CSV Analysis</button>
                        </li>
                    </ul>
                    <div class="tab-content" id="myTabContent">
                        <div class="tab-pane fade show active" id="single" role="tabpanel" aria-labelledby="single-tab">
                            <form id="tweet-form" class="mb-4">
                                <div class="mb-3">
                                    <textarea id="tweet-input" class="form-control" rows="4" placeholder="Enter your text here (no character limit)"></textarea>
                                    <div id="char-count" class="text-muted mt-2"></div>
                                </div>
                                <div class="text-center">
                                    <button type="submit" class="btn btn-primary me-2">
                                        <i class="fas fa-search"></i> Analyze
                                    </button>
                                    <button type="button" id="paste-btn" class="btn btn-secondary">
                                        <i class="fas fa-paste"></i> Paste
                                    </button>
                                </div>
                            </form>
                        </div>
                        <div class="tab-pane fade" id="csv" role="tabpanel" aria-labelledby="csv-tab">
                            <form id="csv-form" class="mb-4" enctype="multipart/form-data">
                                <div class="mb-3">
                                    <label for="file" class="form-label">Upload CSV file:</label>
                                    <input type="file" class="form-control" id="file" name="file" accept=".csv" required>
                                </div>
                                <div class="mb-3">
                                    <label for="text_column" class="form-label">Text column name:</label>
                                    <input type="text" class="form-control" id="text_column" name="text_column" value="text">
                                </div>
                                <div class="mb-3">
                                    <label for="start_row" class="form-label">Start row:</label>
                                    <input type="number" class="form-control" id="start_row" name="start_row" value="0" min="0">
                                </div>
                                <div class="mb-3">
                                    <label for="end_row" class="form-label">End row:</label>
                                    <input type="number" class="form-control" id="end_row" name="end_row" min="1">
                                </div>
                                <button type="submit" class="btn btn-primary">Analyze CSV</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            <div id="results" class="row" style="display: none;">
                <!-- Results will be dynamically inserted here -->
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            const form = document.getElementById('tweet-form');
            const results = document.getElementById('results');
            const pasteBtn = document.getElementById('paste-btn');
            let charts = {};

            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const tweet = document.getElementById('tweet-input').value;
                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({tweet})
                    });
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = await response.json();
                    console.log("Received data:", data);
                    displayResults(data);
                } catch (error) {
                    console.error("Error:", error);
                    results.innerHTML = `<p>Error: ${error.message}</p>`;
                }
            });

            pasteBtn.addEventListener('click', async () => {
                try {
                    const text = await navigator.clipboard.readText();
                    document.getElementById('tweet-input').value = text;
                } catch (err) {
                    console.error('Failed to read clipboard contents: ', err);
                }
            });

            function displayResults(data) {
                if (data.error) {
                    results.innerHTML = `<p>Error: ${data.error}</p>`;
                    return;
                }
                results.style.display = 'flex';
                results.innerHTML = `
                    <div class="col-md-6 mb-4">
                        <div class="dashboard-card">
                            <div class="card-header">
                                <i class="fas fa-chart-pie"></i> AWS Sentiment
                            </div>
                            <div class="card-body">
                                <h2 class="text-center">${data.aws_sentiment}</h2>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-4">
                        <div class="dashboard-card">
                            <div class="card-header">
                                <i class="fas fa-comment-dots"></i> TextBlob Sentiment
                            </div>
                            <div class="card-body">
                                <h2 class="text-center">${data.textblob_sentiment}</h2>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-4">
                        <div class="dashboard-card">
                            <div class="card-header">
                                <i class="fas fa-chart-bar"></i> AWS Sentiment Scores
                            </div>
                            <div class="card-body">
                                <canvas id="aws-sentiment-chart"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-4">
                        <div class="dashboard-card">
                            <div class="card-header">
                                <i class="fas fa-balance-scale"></i> Sentiment Comparison
                            </div>
                            <div class="card-body">
                                <canvas id="sentiment-comparison-chart"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-4">
                        <div class="dashboard-card">
                            <div class="card-header">
                                <i class="fas fa-key"></i> Key Phrases
                            </div>
                            <div class="card-body scroll-box">
                                <ul class="list-group list-group-flush" id="key-phrases-list">
                                    ${data.key_phrases.map(phrase => `<li class="list-group-item">${phrase}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-4">
                        <div class="dashboard-card">
                            <div class="card-header">
                                <i class="fas fa-tags"></i> Entities
                            </div>
                            <div class="card-body scroll-box">
                                <ul class="list-group list-group-flush" id="entities-list">
                                    ${data.entities.map(entity => `<li class="list-group-item">${entity.Text} (${entity.Type})</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-4">
                        <div class="dashboard-card">
                            <div class="card-header">
                                <i class="fas fa-info-circle"></i> Text Stats
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-6">
                                        <h4 class="text-center">${data.word_count}</h4>
                                        <p class="text-center">Words</p>
                                    </div>
                                    <div class="col-6">
                                        <h4 class="text-center">${data.char_count}</h4>
                                        <p class="text-center">Characters</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                updateCharts(data);
                animateResults();
            }

            function updateCharts(data) {
                updateSentimentChart(data.aws_scores);
                updateSentimentComparisonChart(data);
            }

            function updateSentimentChart(scores) {
                const ctx = document.getElementById('aws-sentiment-chart').getContext('2d');
                if (charts.sentiment) charts.sentiment.destroy();
                charts.sentiment = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: Object.keys(scores),
                        datasets: [{
                            label: 'AWS Sentiment Scores',
                            data: Object.values(scores),
                            borderColor: [
                                'rgba(75, 192, 192, 1)',
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 206, 86, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        },
                        animation: {
                            duration: 1500,
                            easing: 'easeOutQuart'
                        }
                    }
                });
            }

            function updateSentimentComparisonChart(data) {
                const ctx = document.getElementById('sentiment-comparison-chart').getContext('2d');
                if (charts.comparison) charts.comparison.destroy();
                charts.comparison = new Chart(ctx, {
                    type: 'radar',
                    data: {
                        labels: ['Positive', 'Negative', 'Neutral', 'Mixed'],
                        datasets: [{
                            label: 'AWS',
                            data: [
                                data.aws_scores.Positive,
                                data.aws_scores.Negative,
                                data.aws_scores.Neutral,
                                data.aws_scores.Mixed
                            ],
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                            pointBorderColor: '#fff',
                            pointHoverBackgroundColor: '#fff',
                            pointHoverBorderColor: 'rgba(75, 192, 192, 1)'
                        }, {
                            label: 'TextBlob',
                            data: [
                                data.textblob_sentiment === 'POSITIVE' ? 1 : 0,
                                data.textblob_sentiment === 'NEGATIVE' ? 1 : 0,
                                data.textblob_sentiment === 'NEUTRAL' ? 1 : 0,
                                0 // TextBlob doesn't have a 'Mixed' category
                            ],
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                            pointBorderColor: '#fff',
                            pointHoverBackgroundColor: '#fff',
                            pointHoverBorderColor: 'rgba(255, 99, 132, 1)'
                        }]
                    },
                    options: {
                        elements: {
                            line: {
                                borderWidth: 3
                            }
                        },
                        animation: {
                            duration: 1500,
                            easing: 'easeOutQuart'
                        }
                    }
                });
            }

            function animateResults() {
                anime({
                    targets: '.dashboard-card',
                    opacity: [0, 1],
                    translateY: [50, 0],
                    delay: anime.stagger(100)
                });

                anime({
                    targets: '#key-phrases-list li, #entities-list li',
                    opacity: [0, 1],
                    translateX: [50, 0],
                    delay: anime.stagger(50)
                });
            }

            // Add real-time character count
            const tweetInput = document.getElementById('tweet-input');
            const charCount = document.createElement('div');
            charCount.classList.add('text-muted', 'mt-2');
            tweetInput.parentNode.insertBefore(charCount, tweetInput.nextSibling);

            tweetInput.addEventListener('input', function() {
                charCount.textContent = `${this.value.length} characters`;
            });

            // Add a feature to save analysis results
            const saveButton = document.createElement('button');
            saveButton.textContent = 'Save Analysis';
            saveButton.classList.add('btn', 'btn-success', 'mt-3');
            saveButton.style.display = 'none';
            form.appendChild(saveButton);

            saveButton.addEventListener('click', function() {
                const results = document.getElementById('results').innerHTML;
                const blob = new Blob([results], {type: 'text/html'});
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = 'sentiment_analysis_results.html';
                a.click();
            });

            // Show save button after analysis
            form.addEventListener('submit', function() {
                saveButton.style.display = 'inline-block';
            });

            // Add a theme toggle feature
            const themeToggle = document.createElement('button');
            themeToggle.textContent = 'Toggle Dark Mode';
            themeToggle.classList.add('btn', 'btn-outline-secondary', 'mt-3', 'ms-3');
            form.appendChild(themeToggle);

            themeToggle.addEventListener('click', function() {
                document.body.classList.toggle('dark-mode');
                updateChartsTheme();
            });

            function updateChartsTheme() {
                const isDarkMode = document.body.classList.contains('dark-mode');
                const textColor = isDarkMode ? '#ffffff' : '#000000';
                
                Object.values(charts).forEach(chart => {
                    chart.options.plugins.legend.labels.color = textColor;
                    chart.options.scales.x.ticks.color = textColor;
                    chart.options.scales.y.ticks.color = textColor;
                    chart.update();
                });
            }

            // Add dark mode styles
            const style = document.createElement('style');
            style.textContent = `
                .dark-mode {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                }
                .dark-mode .dashboard-card {
                    background-color: #34495e;
                }
                .dark-mode .card-header {
                    background-color: #2980b9;
                }
                .dark-mode .btn-primary {
                    background-color: #3498db;
                    border-color: #3498db;
                }
                .dark-mode .btn-primary:hover {
                    background-color: #2980b9;
                    border-color: #2980b9;
                }
            `;
            document.head.appendChild(style);

            // Add event listener for CSV form
            document.getElementById('csv-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                try {
                    const response = await fetch('/', {
                        method: 'POST',
                        body: formData
                    });
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const result = await response.text();
                    document.getElementById('results').innerHTML = result;
                    document.getElementById('results').style.display = 'block';
                } catch (error) {
                    console.error("Error:", error);
                    document.getElementById('results').innerHTML = `<p>Error: ${error.message}</p>`;
                    document.getElementById('results').style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    ''')

@app.route('/analyze', methods=['POST'])
def analyze():
    app.logger.debug("Received request for sentiment analysis")
    data = request.json
    tweet = data['tweet']
    app.logger.debug(f"Analyzing tweet: {tweet}")
    try:
        result = analyze_sentiment(tweet)
        app.logger.debug(f"Analysis result: {result}")
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error during analysis: {str(e)}")
        return jsonify({"error": str(e)}), 500

def generate_visualizations(df):
    visualizations = {}
    
    try:
        # AWS Sentiment Distribution
        plt.figure(figsize=(10, 6))
        df['aws_sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('AWS Sentiment Distribution')
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        visualizations['aws_sentiment'] = base64.b64encode(img.getvalue()).decode()
        plt.close()
    except Exception as e:
        app.logger.error(f"Error generating AWS Sentiment Distribution: {str(e)}")
    
    try:
        # Sentiment Scores Distribution
        plt.figure(figsize=(12, 6))
        scores = pd.DataFrame(df['aws_scores'].tolist(), index=df.index)
        sns.boxplot(data=scores)
        plt.title('Distribution of AWS Sentiment Scores')
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        visualizations['sentiment_scores'] = base64.b64encode(img.getvalue()).decode()
        plt.close()
    except Exception as e:
        app.logger.error(f"Error generating Sentiment Scores Distribution: {str(e)}")
    
    return visualizations

def render_results(df, visualizations):
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SentiTweet - Analysis Results</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>Analysis Results</h1>
            <h2>Visualizations</h2>
            {% for name, img_data in visualizations.items() %}
                <h3>{{ name }}</h3>
                <img src="data:image/png;base64,{{ img_data }}" alt="{{ name }}" class="img-fluid">
            {% endfor %}
            <h2>Raw Data</h2>
            {{ df.to_html(classes="table table-striped") | safe }}
        </div>
    </body>
    </html>
    ''', df=df, visualizations=visualizations)

def run_web_app():
    app.run(debug=True)

if __name__ == '__main__':
    run_web_app()