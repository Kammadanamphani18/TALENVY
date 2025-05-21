# Social Media Sentiment Analyzer

A web application that analyzes sentiment from Reddit comments about products/services using NLP and Flask.

![Main Interface](https://via.placeholder.com/800x500.png?text=Sentiment+Analysis+Input+Form)
![Results Page](https://via.placeholder.com/800x500.png?text=Sentiment+Distribution+Chart+and+Stats)

## Features

- Real-time Reddit comment analysis
- Sentiment classification (Positive/Negative/Neutral)
- Interactive pie chart visualization
- Mobile-responsive design
- User-friendly web interface
- Percentage-based sentiment breakdown

## Technologies Used

- **Python 3**
- **Flask** (Web Framework)
- **PRAW** (Reddit API Wrapper)
- **NLTK** (Natural Language Toolkit)
- **Plotly** (Data Visualization)
- **Bootstrap 5** (Frontend Design)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sentiment-analysis-project.git
cd sentiment-analysis-project
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Reddit API**
- Create `config.ini` in project root:
```ini
[REDDIT]
client_id = your_reddit_client_id
client_secret = your_reddit_client_secret
user_agent = sentiment_analysis_v1
```

## Usage

1. **Run the application**
```bash
python run.py
```

2. **Access the web interface**
```
http://localhost:5000
```

3. **Input parameters**
- Subreddit name (e.g., `technology`)
- Product/brand name (e.g., `iPhone`)
- Number of posts to analyze (default: 50)

## Project Structure

```
sentiment-analysis-project/
├── app/
│   ├── static/       # CSS files
│   ├── templates/    # HTML templates
│   ├── __init__.py
│   ├── reddit_api.py # Reddit API handler
│   └── sentiment_analysis.py # NLP processing
├── config.ini        # API credentials
├── requirements.txt  # Dependencies
└── run.py            # Application entry point
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Support

For issues/questions, please [file an issue](https://github.com/yourusername/sentiment-analysis-project/issues).

---

**Note**: Replace placeholder images with actual screenshots:
1. Take screenshots of your running application
2. Upload to project's `/docs/images` folder
3. Update image URLs in this README