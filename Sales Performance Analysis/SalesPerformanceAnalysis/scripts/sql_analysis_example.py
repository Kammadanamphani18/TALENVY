from sales_analysis import SalesPerformanceAnalysis

# Example using MySQL
connection_string = "mysql+pymysql://root:1234@localhost:3306/retail_database"

# Create an instance with the connection string
analyzer = SalesPerformanceAnalysis(connection_string=connection_string)

# Load data using the default query
analyzer.load_data_from_sql()

# Or provide a custom query
custom_query = """
SELECT 
    s.sale_id,
    s.sale_date,
    p.product_id,
    p.product_name,
    p.category,
    s.quantity,
    s.price,
    s.customer_id,
    c.region,
    m.campaign_id,
    (s.quantity * s.price) as sales_amount
FROM 
    sales s
JOIN 
    products p ON s.product_id = p.product_id
JOIN 
    customers c ON s.customer_id = c.customer_id
LEFT JOIN 
    marketing_campaigns m ON s.sale_date BETWEEN m.start_date AND m.end_date
WHERE 
    s.sale_date >= '2022-01-01'
"""

analyzer.load_data_from_sql(query=custom_query)

# Run your analysis
analyzer.monthly_sales_trend()
analyzer.product_category_analysis()
analyzer.regional_sales_analysis()
analyzer.marketing_campaign_impact()

# Generate comprehensive report
analyzer.generate_comprehensive_report()