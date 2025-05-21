import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import numpy as np
from plotly.subplots import make_subplots

# Load the data
try:
    df = pd.read_csv("large_stock_dataset_2015_2024.csv")
    # Convert 'Date' to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Print column names to debug
    print("Available columns:", df.columns.tolist())
    
    # Rename columns if needed to ensure compatibility
    # yfinance typically uses "Adj Close" (with a space)
    if "Adj Close" in df.columns:
        price_col = "Adj Close"
    elif "Adjusted Close" in df.columns:
        price_col = "Adjusted Close"
    else:
        # Fallback to regular Close if Adj Close isn't available
        price_col = "Close"
    
    print(f"Using {price_col} as the price column")
    
except FileNotFoundError:
    print("CSV file not found. Please run large_stock_data_fetcher.py first.")
    exit()

# Calculate additional metrics
def calculate_metrics(dataframe):
    # Group by ticker and date
    ticker_groups = dataframe.groupby('Ticker')
    
    results = []
    for ticker, group in ticker_groups:
        # Sort by date
        group = group.sort_values('Date')
        
        # Calculate daily returns
        group['Daily_Return'] = group[price_col].pct_change() * 100
        
        # Calculate 20-day and 50-day moving averages
        group['MA20'] = group[price_col].rolling(window=20).mean()
        group['MA50'] = group[price_col].rolling(window=50).mean()
        
        # Calculate RSI (14-day)
        delta = group[price_col].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        group['RSI'] = 100 - (100 / (1 + rs))
        
        results.append(group)
    
    return pd.concat(results)

# Calculate metrics
df = calculate_metrics(df)

# Get min and max dates for the slider
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()
all_tickers = sorted(df['Ticker'].unique())

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = dbc.Container([
    html.H1("Interactive Stock Market Dashboard", className="mt-4 mb-4 text-center"),
    
    dbc.Row([
        dbc.Col([
            html.H4("Select Stocks:"),
            dcc.Dropdown(
                id='ticker-selector',
                options=[{'label': ticker, 'value': ticker} for ticker in all_tickers],
                value=all_tickers[:3],  # Default to first 3 stocks
                multi=True
            ),
        ], width=6),
        
        dbc.Col([
            html.H4("Select Date Range:"),
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                start_date=pd.to_datetime("2023-01-01").date(),
                end_date=max_date
            ),
        ], width=6),
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H4("Select Chart Type:"),
            dcc.RadioItems(
                id='chart-type',
                options=[
                    {'label': 'Price', 'value': 'price'},
                    {'label': 'Returns', 'value': 'returns'},
                    {'label': 'Volume', 'value': 'volume'}
                ],
                value='price',
                inline=True
            ),
        ], width=6),
        
        dbc.Col([
            html.H4("Technical Indicators:"),
            dcc.Checklist(
                id='indicators',
                options=[
                    {'label': '20-Day MA', 'value': 'ma20'},
                    {'label': '50-Day MA', 'value': 'ma50'},
                    {'label': 'RSI', 'value': 'rsi'}
                ],
                value=[],
                inline=True
            ),
        ], width=6),
    ], className="mt-3"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Stock Price/Returns Chart"),
                dbc.CardBody([
                    dcc.Graph(id='main-chart', style={'height': '500px'})
                ])
            ])
        ], width=12)
    ], className="mt-3"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Volume Analysis"),
                dbc.CardBody([
                    dcc.Graph(id='volume-chart', style={'height': '300px'})
                ])
            ])
        ], width=12)
    ], className="mt-3"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Performance Metrics"),
                dbc.CardBody([
                    html.Div(id='performance-metrics')
                ])
            ])
        ], width=12)
    ], className="mt-3 mb-5"),
    
], fluid=True)

# Define callback for main chart
@app.callback(
    Output('main-chart', 'figure'),
    [Input('ticker-selector', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('chart-type', 'value'),
     Input('indicators', 'value')]
)
def update_main_chart(selected_tickers, start_date, end_date, chart_type, indicators):
    if not selected_tickers:
        return go.Figure()
    
    # Filter data based on selections
    filtered_df = df[df['Ticker'].isin(selected_tickers)]
    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
    
    fig = go.Figure()
    
    for ticker in selected_tickers:
        ticker_data = filtered_df[filtered_df['Ticker'] == ticker]
        
        if chart_type == 'price':
            fig.add_trace(go.Scatter(
                x=ticker_data['Date'],
                y=ticker_data[price_col],
                mode='lines',
                name=f'{ticker} Price'
            ))
            
            # Add indicators
            if 'ma20' in indicators:
                fig.add_trace(go.Scatter(
                    x=ticker_data['Date'],
                    y=ticker_data['MA20'],
                    mode='lines',
                    line=dict(width=1, dash='dash'),
                    name=f'{ticker} 20-Day MA'
                ))
            
            if 'ma50' in indicators:
                fig.add_trace(go.Scatter(
                    x=ticker_data['Date'],
                    y=ticker_data['MA50'],
                    mode='lines',
                    line=dict(width=1, dash='dot'),
                    name=f'{ticker} 50-Day MA'
                ))
        
        elif chart_type == 'returns':
            fig.add_trace(go.Scatter(
                x=ticker_data['Date'],
                y=ticker_data['Daily_Return'],
                mode='lines',
                name=f'{ticker} Returns'
            ))
        
        elif chart_type == 'volume':
            fig.add_trace(go.Bar(
                x=ticker_data['Date'],
                y=ticker_data['Volume'],
                name=f'{ticker} Volume'
            ))
    
    # Add RSI as a separate subplot if selected
    if 'rsi' in indicators and chart_type == 'price':
        fig_rsi = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.1, row_heights=[0.7, 0.3])
        
        # Add all existing traces to the first subplot
        for trace in fig.data:
            fig_rsi.add_trace(trace, row=1, col=1)
        
        # Add RSI traces to the second subplot
        for ticker in selected_tickers:
            ticker_data = filtered_df[filtered_df['Ticker'] == ticker]
            fig_rsi.add_trace(go.Scatter(
                x=ticker_data['Date'],
                y=ticker_data['RSI'],
                mode='lines',
                name=f'{ticker} RSI'
            ), row=2, col=1)
        
        # Add horizontal lines at 30 and 70 for RSI
        fig_rsi.add_hline(y=30, line_dash="dash", row=2, col=1, 
                      line=dict(color="green", width=1))
        fig_rsi.add_hline(y=70, line_dash="dash", row=2, col=1,
                      line=dict(color="red", width=1))
        
        fig_rsi.update_layout(
            height=700,
            title_text="Stock Price and RSI",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        return fig_rsi
    
    title_map = {
        'price': 'Stock Price Over Time',
        'returns': 'Daily Returns (%)',
        'volume': 'Trading Volume'
    }
    
    fig.update_layout(
        title=title_map[chart_type],
        xaxis_title='Date',
        yaxis_title='Value',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    
    return fig

# Define callback for volume chart
@app.callback(
    Output('volume-chart', 'figure'),
    [Input('ticker-selector', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_volume_chart(selected_tickers, start_date, end_date):
    if not selected_tickers:
        return go.Figure()
    
    # Filter data based on selections
    filtered_df = df[df['Ticker'].isin(selected_tickers)]
    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
    
    fig = go.Figure()
    
    for ticker in selected_tickers:
        ticker_data = filtered_df[filtered_df['Ticker'] == ticker]
        fig.add_trace(go.Bar(
            x=ticker_data['Date'],
            y=ticker_data['Volume'],
            name=f'{ticker} Volume'
        ))
    
    fig.update_layout(
        title='Trading Volume Over Time',
        xaxis_title='Date',
        yaxis_title='Volume',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        barmode='group'
    )
    
    return fig

# Define callback for performance metrics
@app.callback(
    Output('performance-metrics', 'children'),
    [Input('ticker-selector', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_performance_metrics(selected_tickers, start_date, end_date):
    if not selected_tickers:
        return html.Div("Select at least one ticker to see performance metrics")
    
    # Filter data based on selections
    filtered_df = df[df['Ticker'].isin(selected_tickers)]
    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
    
    metrics_rows = []
    
    for ticker in selected_tickers:
        ticker_data = filtered_df[filtered_df['Ticker'] == ticker].sort_values('Date')
        
        if ticker_data.empty or len(ticker_data) < 2:
            continue
        
        # Calculate metrics
        start_price = ticker_data[price_col].iloc[0]
        end_price = ticker_data[price_col].iloc[-1]
        total_return = ((end_price / start_price) - 1) * 100
        
        daily_returns = ticker_data['Daily_Return'].dropna()
        avg_daily_return = daily_returns.mean()
        volatility = daily_returns.std()
        
        # Calculate max drawdown
        cumulative_returns = (1 + ticker_data['Daily_Return'].dropna() / 100).cumprod()
        running_max = cumulative_returns.cummax()
        drawdown = ((cumulative_returns / running_max) - 1) * 100
        max_drawdown = drawdown.min()
        
        # Create a row for this ticker
        metrics_rows.append(
            dbc.Row([
                dbc.Col(html.H5(ticker), width=2),
                dbc.Col([
                    html.P(f"Total Return: {total_return:.2f}%"),
                ], width=2),
                dbc.Col([
                    html.P(f"Avg Daily Return: {avg_daily_return:.2f}%"),
                ], width=2),
                dbc.Col([
                    html.P(f"Volatility: {volatility:.2f}%"),
                ], width=2),
                dbc.Col([
                    html.P(f"Max Drawdown: {max_drawdown:.2f}%"),
                ], width=2),
                dbc.Col([
                    html.P(f"Start: ${start_price:.2f}, End: ${end_price:.2f}"),
                ], width=2),
            ], className="mb-2")
        )
    
    if not metrics_rows:
        return html.Div("No data available for the selected period")
    
    return html.Div(metrics_rows)

if __name__ == '__main__':
    app.run(debug=True)  # Changed from app.run_server(debug=True)