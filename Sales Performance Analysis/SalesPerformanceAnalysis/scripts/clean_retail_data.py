import pandas as pd
import numpy as np
from datetime import datetime
import os

def clean_retail_data(input_file, output_file):
    """
    Clean the retail dataset by handling missing values,
    correcting data types, and preparing for analysis
    """
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    print("Original data shape:", df.shape)
    
    # 1. Convert date columns to datetime
    date_columns = [col for col in df.columns if 'date' in col.lower()]
    for col in date_columns:
        try:
            df[col] = pd.to_datetime(df[col])
            print(f"Converted {col} to datetime")
        except:
            print(f"Could not convert {col} to datetime")
    
    # 2. Handle missing values
    # For categorical columns, fill with 'Unknown'
    cat_columns = df.select_dtypes(include=['object']).columns
    for col in cat_columns:
        if df[col].isnull().sum() > 0:
            missing_count = df[col].isnull().sum()
            df[col] = df[col].fillna('Unknown')
            print(f"Filled {missing_count} missing values in {col} with 'Unknown'")
    
    # For numeric columns, fill with median
    num_columns = df.select_dtypes(include=['number']).columns
    for col in num_columns:
        if df[col].isnull().sum() > 0:
            missing_count = df[col].isnull().sum()
            median_value = df[col].median()
            df[col] = df[col].fillna(median_value)
            print(f"Filled {missing_count} missing values in {col} with median ({median_value})")
    
    # 3. Calculate sales_amount if not present
    if 'sales_amount' not in df.columns and 'quantity' in df.columns and 'price' in df.columns:
        df['sales_amount'] = df['quantity'] * df['price']
        print("Created 'sales_amount' column from quantity and price")
    
    # 4. Remove duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        print(f"Removed {duplicates} duplicate rows")
    
    # 5. Handle outliers in numerical columns
    for col in ['price', 'quantity', 'sales_amount']:
        if col in df.columns:
            # Use IQR method to identify outliers
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Count outliers
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].shape[0]
            
            if outliers > 0:
                print(f"Identified {outliers} outliers in {col}")
                # Cap outliers instead of removing them
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
                print(f"Capped outliers in {col} to range [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    print(f"Cleaned data shape: {df.shape}")
    
    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
    
    return df

if __name__ == "__main__":
    # UPDATED PATHS
    input_file = "SalesPerformanceAnalysis/data/new_retail_data.csv"
    output_file = "SalesPerformanceAnalysis/data/new_retail_data_cleaned.csv"
    
    clean_retail_data(input_file, output_file)