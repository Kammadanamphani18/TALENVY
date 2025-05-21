from sales_analysis import SalesPerformanceAnalysis

# Example 1: Using CSV data source
# Create an analyzer instance with a CSV file source
analyzer = SalesPerformanceAnalysis(data_source="data/sales_data.csv")
analyzer.load_data_from_file()

# Example 2: Using SQL database
# Uncomment to use with your database
# conn_string = "mysql+pymysql://username:password@localhost/retaildb"
# analyzer = SalesPerformanceAnalysis(connection_string=conn_string)
# analyzer.load_data_from_sql()

# Run individual analyses
analyzer.monthly_sales_trend()
analyzer.product_category_analysis()
analyzer.regional_sales_analysis()
analyzer.marketing_campaign_impact()

# Or generate a comprehensive report with all analyses
# analyzer.generate_comprehensive_report()