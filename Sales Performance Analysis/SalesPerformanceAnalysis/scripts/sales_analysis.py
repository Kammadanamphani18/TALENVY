import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.dates as mdates
from scipy import stats

class SalesPerformanceAnalysis:
    def __init__(self, data_source=None, connection_string=None):
        """
        Initialize the Sales Performance Analysis tool
        
        Parameters:
        data_source (str): Path to CSV file or Excel containing sales data
        connection_string (str): SQL connection string if data is to be extracted from a database
        """
        self.data = None
        self.data_source = data_source
        self.connection_string = connection_string
        self.report_path = "reports/"
        
        # Create reports directory if it doesn't exist
        os.makedirs(self.report_path, exist_ok=True)
        
        # Set plotting style
        sns.set(style="whitegrid")
        plt.rcParams["figure.figsize"] = (12, 8)
        
    def load_data_from_file(self):
        """Load data from CSV or Excel file"""
        if self.data_source.endswith('.csv'):
            self.data = pd.read_csv(self.data_source)
        elif self.data_source.endswith(('.xlsx', '.xls')):
            self.data = pd.read_excel(self.data_source)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel files.")
        
        self._prepare_data()
        print(f"Data loaded successfully with {len(self.data)} records.")
        
    def load_data_from_sql(self, query=None):
        """Extract data from SQL database"""
        if not self.connection_string:
            raise ValueError("SQL connection string not provided")
        
        engine = create_engine(self.connection_string)
        
        if query:
            self.data = pd.read_sql(query, engine)
        else:
            # Default query if none provided
            default_query = """
            SELECT 
                sales.sale_id, 
                sales.sale_date,
                sales.product_id,
                products.product_name,
                products.category,
                sales.quantity,
                sales.price,
                sales.customer_id,
                customers.region,
                marketing.campaign_id
            FROM 
                sales
            JOIN 
                products ON sales.product_id = products.product_id
            JOIN 
                customers ON sales.customer_id = customers.customer_id
            LEFT JOIN 
                marketing ON sales.sale_date BETWEEN marketing.start_date AND marketing.end_date
            """
            self.data = pd.read_sql(default_query, engine)
        
        self._prepare_data()
        print(f"Data loaded successfully from SQL with {len(self.data)} records.")
    
    def _prepare_data(self):
        """Prepare and clean data for analysis"""
        # Convert date columns to datetime
        if 'sale_date' in self.data.columns:
            self.data['sale_date'] = pd.to_datetime(self.data['sale_date'])
            
            # Extract useful date components
            self.data['year'] = self.data['sale_date'].dt.year
            self.data['month'] = self.data['sale_date'].dt.month
            self.data['quarter'] = self.data['sale_date'].dt.quarter
            self.data['day_of_week'] = self.data['sale_date'].dt.dayofweek
            
        # Calculate sales amount if not already present
        if 'sales_amount' not in self.data.columns and 'quantity' in self.data.columns and 'price' in self.data.columns:
            self.data['sales_amount'] = self.data['quantity'] * self.data['price']
        
        # Handle missing values
        self.data = self.data.fillna({
            'campaign_id': 'No Campaign',
            'region': 'Unknown'
        })
    
    def monthly_sales_trend(self, save_plot=True):
        """Analyze and visualize monthly sales trends"""
        if self.data is None:
            raise ValueError("Data not loaded. Please load data first.")
        
        # Group by month and sum sales - fixed to avoid column name conflict
        monthly_sales = self.data.groupby([
            self.data['sale_date'].dt.year.rename('year'), 
            self.data['sale_date'].dt.month.rename('month')
        ])['sales_amount'].sum().reset_index()
        
        # Create date column for proper time-series plotting
        monthly_sales['date'] = pd.to_datetime(monthly_sales['year'].astype(str) + '-' + monthly_sales['month'].astype(str) + '-1')
        
        # Plot
        plt.figure(figsize=(15, 7))
        plt.plot(monthly_sales['date'], monthly_sales['sales_amount'], marker='o', linestyle='-', linewidth=2)
        plt.title('Monthly Sales Trend', fontsize=16)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Format x-axis to show month and year
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_plot:
            plt.savefig(f"{self.report_path}monthly_sales_trend.png", dpi=300, bbox_inches='tight')
            print(f"Monthly sales trend plot saved to {self.report_path}monthly_sales_trend.png")
        
        plt.show()
        
        # Detect seasonality
        self._analyze_seasonality()
        
        return monthly_sales
    
    def _analyze_seasonality(self):
        """Analyze seasonality in sales data"""
        quarterly_sales = self.data.groupby('quarter')['sales_amount'].sum()
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(quarterly_sales.index, quarterly_sales.values, color=sns.color_palette("viridis", 4))
        
        # Add data labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'${height:,.0f}', ha='center', va='bottom', fontsize=11)
        
        plt.title('Quarterly Sales Distribution (Seasonal Analysis)', fontsize=16)
        plt.xlabel('Quarter', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.xticks([1, 2, 3, 4], ['Q1', 'Q2', 'Q3', 'Q4'])
        plt.grid(axis='y', alpha=0.3)
        
        plt.savefig(f"{self.report_path}quarterly_sales_seasonality.png", dpi=300, bbox_inches='tight')
        plt.show()
    
    def product_category_analysis(self, top_n=10, save_plot=True):
        """Analyze sales by product category"""
        if self.data is None or 'category' not in self.data.columns:
            raise ValueError("Data not loaded or missing category information")
        
        # Sales by category
        category_sales = self.data.groupby('category')['sales_amount'].sum().sort_values(ascending=False)
        
        # Plot top N categories
        plt.figure(figsize=(12, 8))
        top_categories = category_sales.head(top_n)
        
        # Create horizontal bar chart
        bars = plt.barh(top_categories.index, top_categories.values, color=sns.color_palette("viridis", len(top_categories)))
        
        # Add data labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + (width * 0.01), bar.get_y() + bar.get_height()/2, 
                    f'${width:,.0f}', va='center', fontsize=10)
        
        plt.title(f'Top {top_n} Product Categories by Sales', fontsize=16)
        plt.xlabel('Total Sales ($)', fontsize=12)
        plt.ylabel('Category', fontsize=12)
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        
        if save_plot:
            plt.savefig(f"{self.report_path}top_product_categories.png", dpi=300, bbox_inches='tight')
            print(f"Product category analysis saved to {self.report_path}top_product_categories.png")
        
        plt.show()
        
        return category_sales
    
    def regional_sales_analysis(self, save_plot=True):
        """Analyze sales performance by region"""
        if self.data is None or 'region' not in self.data.columns:
            raise ValueError("Data not loaded or missing region information")
        
        # Sales by region
        region_sales = self.data.groupby('region')['sales_amount'].sum().sort_values(ascending=False)
        
        # Calculate percentage of total
        total_sales = region_sales.sum()
        region_sales_pct = (region_sales / total_sales * 100).round(1)
        
        # Create a pie chart
        plt.figure(figsize=(12, 10))
        plt.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%', 
                startangle=90, shadow=False, explode=[0.05]*len(region_sales),
                colors=sns.color_palette("viridis", len(region_sales)))
        
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Sales Distribution by Region', fontsize=16)
        plt.tight_layout()
        
        if save_plot:
            plt.savefig(f"{self.report_path}regional_sales_distribution.png", dpi=300, bbox_inches='tight')
            print(f"Regional sales analysis saved to {self.report_path}regional_sales_distribution.png")
        
        plt.show()
        
        # Create a DataFrame with both absolute and percentage values
        result_df = pd.DataFrame({
            'Total_Sales': region_sales,
            'Percentage': region_sales_pct
        }).sort_values('Total_Sales', ascending=False)
        
        return result_df
    
    def marketing_campaign_impact(self, save_plot=True):
        """Analyze the impact of marketing campaigns on sales"""
        if self.data is None or 'campaign_id' not in self.data.columns:
            raise ValueError("Data not loaded or missing campaign information")
        
        # Summarize sales by campaign
        campaign_sales = self.data.groupby('campaign_id')['sales_amount'].agg(['sum', 'mean', 'count']).sort_values('sum', ascending=False)
        campaign_sales = campaign_sales.rename(columns={'sum': 'total_sales', 'mean': 'avg_sale', 'count': 'num_transactions'})
        
        # Exclude 'No Campaign' for visualization if it exists
        plot_data = campaign_sales.copy()
        if 'No Campaign' in plot_data.index:
            no_campaign_data = plot_data.loc['No Campaign']
            plot_data = plot_data.drop('No Campaign')
        
        # Plot campaign effectiveness
        plt.figure(figsize=(14, 8))
        
        # Create bar chart for total sales by campaign
        ax1 = plt.subplot(121)
        bars = ax1.bar(plot_data.index, plot_data['total_sales'], color=sns.color_palette("viridis", len(plot_data)))
        
        # Add data labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'${height:,.0f}', ha='center', va='bottom', fontsize=9)
        
        ax1.set_title('Total Sales by Marketing Campaign', fontsize=14)
        ax1.set_xlabel('Campaign ID', fontsize=12)
        ax1.set_ylabel('Total Sales ($)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        # Create bar chart for average transaction value by campaign
        ax2 = plt.subplot(122)
        bars = ax2.bar(plot_data.index, plot_data['avg_sale'], color=sns.color_palette("plasma", len(plot_data)))
        
        # Add data labels
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'${height:,.2f}', ha='center', va='bottom', fontsize=9)
        
        ax2.set_title('Average Sale by Marketing Campaign', fontsize=14)
        ax2.set_xlabel('Campaign ID', fontsize=12)
        ax2.set_ylabel('Average Sale Value ($)', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_plot:
            plt.savefig(f"{self.report_path}marketing_campaign_impact.png", dpi=300, bbox_inches='tight')
            print(f"Marketing campaign analysis saved to {self.report_path}marketing_campaign_impact.png")
        
        plt.show()
        
        # Calculate lift over no campaign
        if 'No Campaign' in campaign_sales.index:
            baseline = no_campaign_data['avg_sale']
            campaign_sales['sales_lift_pct'] = ((campaign_sales['avg_sale'] - baseline) / baseline * 100).round(2)
        
        return campaign_sales
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive sales analysis report with all analyses"""
        if self.data is None:
            raise ValueError("Data not loaded. Please load data first.")
        
        print("Generating comprehensive sales analysis report...")
        
        # Run all analyses
        monthly_trend = self.monthly_sales_trend(save_plot=True)
        category_analysis = self.product_category_analysis(save_plot=True)
        regional_analysis = self.regional_sales_analysis(save_plot=True)
        campaign_impact = self.marketing_campaign_impact(save_plot=True)
        
        # Generate summary statistics
        total_sales = self.data['sales_amount'].sum()
        avg_sale = self.data['sales_amount'].mean()
        total_transactions = len(self.data)
        
        # Create Excel report with multiple sheets

        with pd.ExcelWriter(f"{self.report_path}sales_analysis_report.xlsx") as writer:
            monthly_trend.to_excel(writer, sheet_name='Monthly Sales Trend', index=False)
            category_analysis.to_excel(writer, sheet_name='Product Category Analysis', index=False)
            regional_analysis.to_excel(writer, sheet_name='Regional Sales Analysis', index=False)
            campaign_impact.to_excel(writer, sheet_name='Marketing Campaign Impact', index=False)
            
            # Add summary statistics to a separate sheet
            summary_stats = pd.DataFrame({
                'Metric': ['Total Sales', 'Average Sale', 'Total Transactions'],
                'Value': [total_sales, avg_sale, total_transactions]
            })
            summary_stats.to_excel(writer, sheet_name='Summary Statistics', index=False)
        
        print(f"Comprehensive sales analysis report generated and saved to {self.report_path}sales_analysis_report.xlsx")
