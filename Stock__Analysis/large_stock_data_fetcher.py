import yfinance as yf
import pandas as pd

# List of tickers
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "JPM", "V", "NFLX"]

# Date range
start_date = "2015-01-01"
end_date = "2024-12-31"

# Download and merge data
all_data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')

combined_data = []

for ticker in tickers:
    df = all_data[ticker].copy()
    df['Ticker'] = ticker
    df = df.reset_index()
    combined_data.append(df)

# Combine all into one DataFrame
final_data = pd.concat(combined_data, ignore_index=True)

# Save to CSV
final_data.to_csv("large_stock_dataset_2015_2024.csv", index=False)

print("CSV file saved as large_stock_dataset_2015_2024.csv")
