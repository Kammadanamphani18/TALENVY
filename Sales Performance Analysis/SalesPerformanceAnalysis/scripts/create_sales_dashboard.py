import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter

# Set up paths
DATA_FILE = "SalesPerformanceAnalysis/data/new_retail_data.csv"
OUTPUT_DIR = "sales_dashboard"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set plotting style
plt.style.use('ggplot')
sns.set_palette("Set2")

def load_and_prepare_data():
    """Load and prepare the retail data for analysis"""
    print(f"Loading data from {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    
    # Handle missing values
    df = df.dropna(subset=['Amount', 'Product_Category', 'Date'])
    
    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Create year-month column for trend analysis
    df['YearMonth'] = df['Date'].dt.to_period('M')
    
    # Ensure Amount is numeric
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    return df

def create_dashboard(df):
    """Create a comprehensive sales dashboard with multiple charts"""
    print("Creating sales dashboard...")
    
    # Create a large figure for the dashboard
    fig = plt.figure(figsize=(20, 18))
    gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1])
    
    # 1. KPI Cards at the top
    create_kpi_section(fig, gs[0, :], df)
    
    # 2. Monthly Sales Trend - Line Chart
    ax1 = fig.add_subplot(gs[1, 0])
    create_monthly_trend(ax1, df)
    
    # 3. Product Category Comparison - Bar Chart
    ax2 = fig.add_subplot(gs[1, 1])
    create_category_comparison(ax2, df)
    
    # 4. Region-wise Sales (using Country as region) - Bar Chart
    ax3 = fig.add_subplot(gs[2, 0])
    create_region_sales(ax3, df)
    
    # 5. Customer Order Value Distribution - Histogram
    ax4 = fig.add_subplot(gs[2, 1])
    create_order_distribution(ax4, df)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/sales_dashboard.png", dpi=300, bbox_inches='tight')
    print(f"Dashboard saved to {OUTPUT_DIR}/sales_dashboard.png")
    
    # Create additional separate charts
    create_campaign_impact_chart(df)
    create_customer_segment_chart(df)
    
    return fig

def money_formatter(x, pos):
    """Format numbers as currency"""
    return f"${x:,.0f}"

def create_kpi_section(fig, grid_position, df):
    """Create KPI cards section at the top of the dashboard"""
    ax = fig.add_subplot(grid_position)
    ax.axis('off')
    
    # Calculate KPIs
    total_sales = df['Amount'].sum()
    avg_order = df['Amount'].mean()
    total_customers = df['Customer_ID'].nunique()
    total_transactions = len(df)
    
    # Create text for KPIs
    kpi_text = (
        f"SALES PERFORMANCE DASHBOARD\n\n"
        f"Total Sales: ${total_sales:,.2f}\n\n"
        f"Average Order: ${avg_order:,.2f}\n\n"
        f"Total Customers: {total_customers:,}\n\n"
        f"Total Transactions: {total_transactions:,}"
    )
    
    ax.text(0.5, 0.5, kpi_text, ha='center', va='center', 
            fontsize=16, fontweight='bold', 
            bbox=dict(facecolor='lightblue', alpha=0.5, boxstyle='round,pad=1'))

def create_monthly_trend(ax, df):
    """Create monthly sales trend line chart"""
    # Group by year-month and sum sales
    monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum().reset_index()
    monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()
    
    # Plot
    ax.plot(monthly_sales['Date'], monthly_sales['Amount'], marker='o', linewidth=2)
    ax.set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Sales Amount')
    ax.yaxis.set_major_formatter(FuncFormatter(money_formatter))
    ax.grid(True, alpha=0.3)
    
    # Rotate x-tick labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

def create_category_comparison(ax, df):
    """Create product category comparison bar chart"""
    # Group by category and sum sales
    category_sales = df.groupby('Product_Category')['Amount'].sum().sort_values(ascending=False)
    
    # Plot
    bars = ax.bar(category_sales.index, category_sales.values, color=sns.color_palette("Set2", len(category_sales)))
    
    # Add data labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=10)
    
    ax.set_title('Sales by Product Category', fontsize=14, fontweight='bold')
    ax.set_xlabel('Category')
    ax.set_ylabel('Sales Amount')
    ax.yaxis.set_major_formatter(FuncFormatter(money_formatter))
    ax.grid(axis='y', alpha=0.3)
    
    # Rotate x-tick labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

def create_region_sales(ax, df):
    """Create region sales bar chart (using Country as region)"""
    # Group by country and sum sales
    region_sales = df.groupby('Country')['Amount'].sum().sort_values(ascending=False)
    
    # Plot
    bars = ax.bar(region_sales.index, region_sales.values, color=sns.color_palette("Set3", len(region_sales)))
    
    # Add data labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=10)
    
    ax.set_title('Sales by Country', fontsize=14, fontweight='bold')
    ax.set_xlabel('Country')
    ax.set_ylabel('Sales Amount')
    ax.yaxis.set_major_formatter(FuncFormatter(money_formatter))
    ax.grid(axis='y', alpha=0.3)

def create_order_distribution(ax, df):
    """Create order value distribution histogram"""
    # Plot
    sns.histplot(df['Amount'], bins=30, kde=True, ax=ax)
    
    # Add lines for mean and median
    mean_val = df['Amount'].mean()
    median_val = df['Amount'].median()
    
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Mean: ${mean_val:.2f}')
    ax.axvline(median_val, color='green', linestyle='--', linewidth=1.5, label=f'Median: ${median_val:.2f}')
    
    ax.set_title('Order Value Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('Order Amount')
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.xaxis.set_major_formatter(FuncFormatter(money_formatter))

def create_campaign_impact_chart(df):
    """Create a separate chart for campaign impact analysis (using Feedback as proxy for campaign)"""
    if 'Feedback' not in df.columns:
        return
    
    plt.figure(figsize=(12, 8))
    
    # Group by feedback type and calculate average order value
    feedback_impact = df.groupby('Feedback')['Amount'].agg(['mean', 'count']).reset_index()
    
    # Use count as the size of the bubbles
    sizes = feedback_impact['count'] / feedback_impact['count'].max() * 500
    
    # Plot
    plt.scatter(feedback_impact['Feedback'], feedback_impact['mean'], s=sizes, alpha=0.6)
    
    # Add labels
    for i, row in feedback_impact.iterrows():
        plt.text(i, row['mean'], f"${row['mean']:.2f}\n({row['count']} orders)", 
                 ha='center', va='center', fontsize=10)
    
    plt.title('Average Order Value by Feedback Type', fontsize=16, fontweight='bold')
    plt.xlabel('Feedback Type')
    plt.ylabel('Average Order Value')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig(f"{OUTPUT_DIR}/feedback_impact.png", dpi=300, bbox_inches='tight')

def create_customer_segment_chart(df):
    """Create a separate chart for customer segment analysis"""
    if 'Customer_Segment' not in df.columns:
        return
    
    plt.figure(figsize=(12, 8))
    
    # Group by segment and sum sales
    segment_sales = df.groupby('Customer_Segment')['Amount'].sum().sort_values(ascending=False)
    
    # Create pie chart
    plt.pie(segment_sales, labels=segment_sales.index, autopct='%1.1f%%', 
            textprops={'fontsize': 14}, explode=[0.05] * len(segment_sales),
            colors=sns.color_palette("pastel", len(segment_sales)))
    
    plt.title('Sales Distribution by Customer Segment', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig(f"{OUTPUT_DIR}/customer_segment.png", dpi=300, bbox_inches='tight')

def main():
    # Load and prepare data
    df = load_and_prepare_data()
    
    # Create and save the dashboard
    create_dashboard(df)
    
    # Generate additional individual charts
    print("Generating additional individual charts...")
    
    # Monthly trend chart
    plt.figure(figsize=(14, 8))
    monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum().reset_index()
    monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()
    
    plt.plot(monthly_sales['Date'], monthly_sales['Amount'], marker='o', linewidth=2)
    plt.title('Monthly Sales Trend', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Sales Amount', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(money_formatter))
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/monthly_trend.png", dpi=300)
    
    # Top 5 products
    plt.figure(figsize=(14, 8))
    product_sales = df.groupby('products')['Amount'].sum().sort_values(ascending=False).head(10)
    
    bars = plt.barh(product_sales.index, product_sales.values, color=sns.color_palette("viridis", len(product_sales)))
    
    # Add data labels
    for bar in bars:
        width = bar.get_width()
        plt.text(width + (width * 0.01), bar.get_y() + bar.get_height()/2, 
                f'${width:,.0f}', va='center', fontsize=10)
    
    plt.title('Top 10 Products by Sales', fontsize=16, fontweight='bold')
    plt.xlabel('Sales Amount', fontsize=12)
    plt.gca().xaxis.set_major_formatter(FuncFormatter(money_formatter))
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/top_products.png", dpi=300)
    
    print(f"All charts have been saved to the {OUTPUT_DIR} directory.")

if __name__ == "__main__":
    main()