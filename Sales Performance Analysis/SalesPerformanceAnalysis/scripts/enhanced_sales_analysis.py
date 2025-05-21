import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from scipy import stats

class EnhancedSalesAnalysis:
    """Enhanced Sales Analysis class incorporating features from Excel dashboard"""
    
    def __init__(self, data=None, data_source=None):
        """
        Initialize the Enhanced Sales Analysis tool
        
        Parameters:
        data (pd.DataFrame): Preprocessed sales data
        data_source (str): Path to data file if data is not directly provided
        """
        self.data = data
        self.data_source = data_source
        self.report_path = "reports/"
        
        # Create reports directory if it doesn't exist
        os.makedirs(self.report_path, exist_ok=True)
        
        # Set plotting style
        sns.set(style="whitegrid")
        plt.rcParams["figure.figsize"] = (12, 8)
        
        if data_source and not data:
            self.load_data()
            
    def load_data(self):
        """Load data from source file"""
        if self.data_source.endswith('.csv'):
            self.data = pd.read_csv(self.data_source)
        elif self.data_source.endswith(('.xlsx', '.xlsm', '.xls')):
            self.data = pd.read_excel(self.data_source, engine='openpyxl')
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel files.")
        
        self._prepare_data()
        print(f"Data loaded successfully with {len(self.data)} records.")
        
    def _prepare_data(self):
        """Prepare and clean data for analysis"""
        # Convert date columns to datetime - identify date columns
        date_columns = [col for col in self.data.columns if 'date' in col.lower()]
        
        for col in date_columns:
            try:
                self.data[col] = pd.to_datetime(self.data[col])
            except:
                print(f"Could not convert {col} to datetime.")
        
        # Identify the primary date column (order date or sale date)
        primary_date_col = None
        for col in ['sale_date', 'order_date', 'date']:
            if col in self.data.columns:
                primary_date_col = col
                break
        
        if primary_date_col:
            # Extract useful date components
            self.data['year'] = self.data[primary_date_col].dt.year
            self.data['month'] = self.data[primary_date_col].dt.month
            self.data['quarter'] = self.data[primary_date_col].dt.quarter
            self.data['day_of_week'] = self.data[primary_date_col].dt.dayofweek
        
        # Check if we have order and ship dates to calculate shipping duration
        if 'order_date' in self.data.columns and 'ship_date' in self.data.columns:
            self.data['shipping_days'] = (self.data['ship_date'] - self.data['order_date']).dt.days
            
            # Create shipping interval categories as seen in the Excel dashboard
            self.data['shipping_interval'] = pd.cut(
                self.data['shipping_days'],
                bins=[0, 7, 30, float('inf')],
                labels=['Within 7 days', 'Within 30 days', 'After 30 days']
            )
    
    def calculate_key_metrics(self):
        """Calculate key business metrics for the dashboard"""
        metrics = {}
        
        # Detect sales/revenue column
        sales_col = next((col for col in self.data.columns if 'revenue' in col.lower() or 'sales' in col.lower()), None)
        cost_col = next((col for col in self.data.columns if 'cost' in col.lower() or 'cogs' in col.lower()), None)
        profit_col = next((col for col in self.data.columns if 'profit' in col.lower()), None)
        
        if sales_col:
            metrics['total_sales'] = self.data[sales_col].sum()
            metrics['avg_sale'] = self.data[sales_col].mean()
        
        if cost_col:
            metrics['total_cost'] = self.data[cost_col].sum()
        
        if profit_col:
            metrics['total_profit'] = self.data[profit_col].sum()
        elif sales_col and cost_col:
            metrics['total_profit'] = metrics['total_sales'] - metrics['total_cost']
        
        metrics['total_transactions'] = len(self.data)
        
        # If we have shipping days data, calculate shipping metrics
        if 'shipping_days' in self.data.columns:
            metrics['avg_shipping_days'] = self.data['shipping_days'].mean()
            
            # Calculate percentages for shipping intervals
            shipping_counts = self.data['shipping_interval'].value_counts(normalize=True) * 100
            metrics['pct_shipped_within_7_days'] = shipping_counts.get('Within 7 days', 0)
            metrics['pct_shipped_within_30_days'] = shipping_counts.get('Within 30 days', 0)
            metrics['pct_shipped_after_30_days'] = shipping_counts.get('After 30 days', 0)
        
        return metrics
    
    def shipping_interval_analysis(self, save_plot=True):
        """
        Analyze orders by shipping intervals: within 7 days, within 30 days, and after 30 days
        Similar to the Excel dashboard's shipping analysis
        """
        if 'shipping_interval' not in self.data.columns:
            print("Shipping interval data not available.")
            return None
        
        # Group by shipping interval
        interval_counts = self.data['shipping_interval'].value_counts().sort_index()
        
        # Plot
        plt.figure(figsize=(12, 8))
        bars = plt.bar(interval_counts.index, interval_counts.values, 
                color=sns.color_palette("viridis", len(interval_counts)))
        
        # Add data labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{height:,.0f}', ha='center', va='bottom', fontsize=12)
        
        plt.title('Orders by Shipping Interval', fontsize=16)
        plt.ylabel('Number of Orders', fontsize=14)
        plt.grid(axis='y', alpha=0.3)
        
        if save_plot:
            plt.savefig(f"{self.report_path}shipping_interval_analysis.png", dpi=300, bbox_inches='tight')
        
        plt.show()
        
        # Calculate percentages
        interval_pct = interval_counts / interval_counts.sum() * 100
        
        # Return both counts and percentages
        result = pd.DataFrame({
            'Count': interval_counts,
            'Percentage': interval_pct.round(1)
        })
        
        return result
    
    def sales_by_channel(self, metric='sales', save_plot=True):
        """
        Analyze sales performance by sales channel
        Similar to the Excel dashboard's sales channel analysis
        
        Parameters:
        metric (str): Which metric to analyze - 'sales', 'profit', 'transactions', 'cogs'
        """
        # Identify the columns for channel and the requested metric
        channel_col = next((col for col in self.data.columns if 'channel' in col.lower()), None)
        
        if not channel_col:
            print("Sales channel data not available.")
            return None
        
        # Map metric to column
        metric_col = None
        if metric.lower() == 'sales':
            metric_col = next((col for col in self.data.columns if 'revenue' in col.lower() or 'sales' in col.lower()), None)
        elif metric.lower() == 'profit':
            metric_col = next((col for col in self.data.columns if 'profit' in col.lower()), None)
        elif metric.lower() == 'cogs' or metric.lower() == 'cost':
            metric_col = next((col for col in self.data.columns if 'cost' in col.lower() or 'cogs' in col.lower()), None)
        
        if not metric_col and metric.lower() != 'transactions':
            print(f"{metric} data not available.")
            return None
        
        # Group by channel
        if metric.lower() == 'transactions':
            channel_data = self.data.groupby(channel_col).size().sort_values(ascending=False)
            metric_label = 'Number of Transactions'
        else:
            channel_data = self.data.groupby(channel_col)[metric_col].sum().sort_values(ascending=False)
            metric_label = f"Total {metric.capitalize()}"
        
        # Plot
        plt.figure(figsize=(12, 8))
        bars = plt.bar(channel_data.index, channel_data.values, 
                color=sns.color_palette("viridis", len(channel_data)))
        
        # Add data labels
        for bar in bars:
            height = bar.get_height()
            if metric.lower() in ['sales', 'profit', 'cogs', 'cost']:
                label = f'${height:,.0f}'
            else:
                label = f'{height:,.0f}'
            
            plt.text(bar.get_x() + bar.get_width()/2., height + (height * 0.01),
                    label, ha='center', va='bottom', fontsize=12)
        
        plt.title(f'{metric_label} by Sales Channel', fontsize=16)
        plt.ylabel(metric_label, fontsize=14)
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save_plot:
            plt.savefig(f"{self.report_path}{metric.lower()}_by_sales_channel.png", dpi=300, bbox_inches='tight')
        
        plt.show()
        
        return channel_data
    
    def monthly_quarterly_analysis(self, metric='sales', period='monthly', save_plot=True):
        """
        Analyze monthly or quarterly trends
        Similar to the Excel dashboard's time-based analysis
        
        Parameters:

        metric (str): Which metric to analyze"""