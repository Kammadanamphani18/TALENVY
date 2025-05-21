import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Generate date range
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') 
              for i in range((end_date - start_date).days + 1)]

# Sample products
products = [
    {'product_id': 1, 'product_name': 'Laptop', 'category': 'Electronics'},
    {'product_id': 2, 'product_name': 'Smartphone', 'category': 'Electronics'},
    {'product_id': 3, 'product_name': 'T-shirt', 'category': 'Clothing'},
    {'product_id': 4, 'product_name': 'Jeans', 'category': 'Clothing'},
    {'product_id': 5, 'product_name': 'Coffee Maker', 'category': 'Home Appliances'},
    {'product_id': 6, 'product_name': 'Refrigerator', 'category': 'Home Appliances'},
    {'product_id': 7, 'product_name': 'Book', 'category': 'Books'},
    {'product_id': 8, 'product_name': 'Chocolate', 'category': 'Food'},
    {'product_id': 9, 'product_name': 'Headphones', 'category': 'Electronics'},
    {'product_id': 10, 'product_name': 'Sofa', 'category': 'Furniture'}
]

# Regions
regions = ['North', 'South', 'East', 'West', 'Central']

# Marketing campaigns
campaigns = ['Summer Sale', 'Back to School', 'Holiday Season', 'Spring Promotion', 'No Campaign']

# Generate 5000 sales records
num_records = 5000
data = []

for i in range(num_records):
    # Select random date with higher probability for certain periods (seasonality)
    month_weights = [0.06, 0.05, 0.07, 0.08, 0.09, 0.1, 0.08, 0.12, 0.09, 0.08, 0.08, 0.1]
    month = np.random.choice(range(1, 13), p=month_weights)
    
    # Adjust date selection to create seasonality
    if month in [11, 12]:  # Holiday season
        sale_date = np.random.choice([d for d in date_range if d.startswith(f'2022-{month:02d}') or 
                                    d.startswith(f'2023-{month:02d}')])
    elif month in [8, 9]:  # Back to school
        sale_date = np.random.choice([d for d in date_range if d.startswith(f'2022-{month:02d}') or 
                                    d.startswith(f'2023-{month:02d}')])
    else:
        sale_date = np.random.choice(date_range)
    
    # Select random product with different probabilities
    product = np.random.choice(products)
    
    # Quantity varies by product category
    if product['category'] == 'Electronics':
        quantity = np.random.randint(1, 3)
    elif product['category'] == 'Food':
        quantity = np.random.randint(1, 10)
    else:
        quantity = np.random.randint(1, 5)
    
    # Price varies by product
    if product['product_id'] == 1:  # Laptop
        price = np.random.uniform(800, 1500)
    elif product['product_id'] == 2:  # Smartphone
        price = np.random.uniform(500, 1200)
    elif product['product_id'] in [3, 4]:  # Clothing
        price = np.random.uniform(20, 80)
    elif product['product_id'] in [5, 6]:  # Home Appliances
        price = np.random.uniform(100, 500)
    else:
        price = np.random.uniform(10, 200)
    
    # Region with different distribution
    region = np.random.choice(regions, p=[0.3, 0.25, 0.15, 0.2, 0.1])
    
    # Campaign assignment
    month_num = int(sale_date.split('-')[1])
    if month_num in [6, 7]:
        campaign_id = 'Summer Sale'
    elif month_num in [8, 9]:
        campaign_id = 'Back to School'
    elif month_num in [11, 12]:
        campaign_id = 'Holiday Season'
    elif month_num in [3, 4]:
        campaign_id = 'Spring Promotion'
    else:
        campaign_id = np.random.choice(['No Campaign', 'No Campaign', 'No Campaign', 
                                       'Summer Sale', 'Back to School', 'Holiday Season', 'Spring Promotion'])
    
    # Calculate sales amount
    sales_amount = price * quantity
    
    # Create record
    record = {
        'sale_id': i+1,
        'sale_date': sale_date,
        'product_id': product['product_id'],
        'product_name': product['product_name'],
        'category': product['category'],
        'quantity': quantity,
        'price': round(price, 2),
        'customer_id': np.random.randint(1, 1001),
        'region': region,
        'campaign_id': campaign_id,
        'sales_amount': round(sales_amount, 2)
    }
    
    data.append(record)

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('data/sales_data.csv', index=False)

print("Sample sales data generated and saved to data/sales_data.csv")