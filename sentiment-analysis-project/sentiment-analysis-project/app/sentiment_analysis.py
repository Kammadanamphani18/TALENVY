import nltk
import ssl

# Bypass SSL verification for NLTK downloads
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('vader_lexicon')  # This should execute BEFORE creating SentimentIntensityAnalyzer

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiments(comments):
    sia = SentimentIntensityAnalyzer()
    results = []
    
    for comment in comments:
        text = comment['text']
        score = sia.polarity_scores(text)
        
        if score['compound'] >= 0.05:
            sentiment = 'positive'
        elif score['compound'] <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        results.append({
            'text': text,
            'sentiment': sentiment,
            'scores': score
        })
    
    return results