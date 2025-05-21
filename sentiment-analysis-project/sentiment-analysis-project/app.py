import sys
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.utils
from flask import Flask, render_template, request
from app.reddit_api import get_reddit_comments
from app.sentiment_analysis import analyze_sentiments
import json

# Add path configuration
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

app = Flask(__name__, template_folder=os.path.abspath('app/templates'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    subreddit = request.form['subreddit']
    product = request.form['product']
    limit = int(request.form['limit'])
    
    # Get data from Reddit
    comments = get_reddit_comments(subreddit, product, limit)
    
    # Perform sentiment analysis
    analyzed_data = analyze_sentiments(comments)
    
    # Generate enhanced visualization
    sentiments = [item['sentiment'] for item in analyzed_data]
    pos = sentiments.count('positive')
    neg = sentiments.count('negative')
    neu = sentiments.count('neutral')
    total = len(sentiments)

    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type':'domain'}, {'type':'xy'}]],
        subplot_titles=('Sentiment Distribution', 'Sentiment Intensity')
    )

    # Add pie chart
    fig.add_trace(go.Pie(
        labels=['Positive', 'Negative', 'Neutral'],
        values=[pos, neg, neu],
        marker_colors=['#2ecc71', '#e74c3c', '#3498db'],
        hole=.4,
        textinfo='percent+value',
        hoverinfo='label+percent'
    ), 1, 1)

    # Add bar chart
    fig.add_trace(go.Bar(
        x=['Positive', 'Negative', 'Neutral'],
        y=[pos, neg, neu],
        marker_color=['#2ecc71', '#e74c3c', '#3498db'],
        text=[pos, neg, neu],
        textposition='auto'
    ), 1, 2)

    # Update layout
    fig.update_layout(
        height=500,
        showlegend=False,
        margin=dict(t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12, color="#2c3e50")
    )

    # Convert to JSON
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('results.html',
                         chart_json=chart_json,
                         total=total,
                         pos=pos,
                         neg=neg,
                         neu=neu)

if __name__ == '__main__':
    app.run(debug=True)