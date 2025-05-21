import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sales_analysis import SalesPerformanceAnalysis
from enhanced_sales_analysis import EnhancedSalesAnalysis

# Set up paths - UPDATED PATH
DATA_FILE = "SalesPerformanceAnalysis/data/new_retail_data.csv"
OUTPUT_DIR = "analysis_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def explore_data(df):
    """Perform initial data exploration and return summary statistics"""
    print("=" * 50)
    print("DATA EXPLORATION")
    print("=" * 50)
    
    # Basic information
    print(f"Dataset shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    # Data types and missing values
    print("\nData types and missing values:")
    missing_data = pd.DataFrame({
        'Data Type': df.dtypes,
        'Missing Values': df.isnull().sum(),
        'Missing Percentage': (df.isnull().sum() / len(df) * 100).round(2)
    })
    print(missing_data)
    
    # Summary statistics
    print("\nSummary statistics for numerical columns:")
    print(df.describe())
    
    # Categorical columns
    cat_columns = df.select_dtypes(include=['object']).columns
    if len(cat_columns) > 0:
        print("\nUnique values in categorical columns:")
        for col in cat_columns:
            print(f"\n{col}: {df[col].nunique()} unique values")
            print(df[col].value_counts().head(10))
    
    return missing_data

def main():
    print(f"Loading data from {DATA_FILE}...")
    
    # Load the raw data for exploration
    try:
        raw_data = pd.read_csv(DATA_FILE)
        # Save exploration results
        missing_data = explore_data(raw_data)
        missing_data.to_csv(f"{OUTPUT_DIR}/missing_data_summary.csv")
    except Exception as e:
        print(f"Error during data exploration: {e}")
        return
    
    # Use the SalesPerformanceAnalysis class for main analysis
    try:
        print("\nRunning main sales performance analysis...")
        analyzer = SalesPerformanceAnalysis(data_source=DATA_FILE)
        analyzer.load_data_from_file()
        
        # Set report path to our output directory
        analyzer.report_path = f"{OUTPUT_DIR}/"
        
        # Run individual analyses
        analyzer.monthly_sales_trend()
        analyzer.product_category_analysis()
        analyzer.regional_sales_analysis()
        analyzer.marketing_campaign_impact()
        
        # Generate comprehensive report
        analyzer.generate_comprehensive_report()
        
        print(f"\nBasic sales analysis complete. Results saved to {OUTPUT_DIR}/")
    except Exception as e:
        print(f"Error during sales performance analysis: {e}")
    
    # Use the EnhancedSalesAnalysis for additional insights
    try:
        print("\nRunning enhanced sales analysis...")
        enhanced_analyzer = EnhancedSalesAnalysis(data_source=DATA_FILE)
        enhanced_analyzer.report_path = f"{OUTPUT_DIR}/enhanced_"
        
        # Calculate key metrics
        metrics = enhanced_analyzer.calculate_key_metrics()
        print("\nKey Business Metrics:")
        for key, value in metrics.items():
            print(f"{key}: {value}")
        
        # Save metrics to CSV
        pd.DataFrame([metrics]).to_csv(f"{OUTPUT_DIR}/key_business_metrics.csv", index=False)
        
        # Run enhanced analyses
        if 'shipping_days' in enhanced_analyzer.data.columns:
            enhanced_analyzer.shipping_interval_analysis()
        
        # Analyze sales by channel if data available
        channel_col = next((col for col in enhanced_analyzer.data.columns if 'channel' in col.lower()), None)
        if channel_col:
            enhanced_analyzer.sales_by_channel()
        
        # Run monthly/quarterly analysis
        enhanced_analyzer.monthly_quarterly_analysis(period='monthly')
        enhanced_analyzer.monthly_quarterly_analysis(period='quarterly')
        
        print(f"\nEnhanced analysis complete. Additional results saved to {OUTPUT_DIR}/")
    except Exception as e:
        print(f"Error during enhanced sales analysis: {e}")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()