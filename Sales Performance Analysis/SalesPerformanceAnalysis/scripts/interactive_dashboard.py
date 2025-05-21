import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set up paths
DATA_FILE = "SalesPerformanceAnalysis/data/new_retail_data.csv"

@st.cache_data
def load_data():
    """Load and prepare the retail data for analysis"""
    try:
        df = pd.read_csv(DATA_FILE)
        
        # Handle missing values in essential columns
        df = df.dropna(subset=['Amount', 'Product_Category', 'Date'])
        
        # Convert date to datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Create year-month column for trend analysis
        df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Quarter'] = df['Date'].dt.quarter
        
        # Ensure Amount is numeric
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Return an empty DataFrame with expected columns to prevent further errors
        return pd.DataFrame(columns=['Amount', 'Product_Category', 'Date', 'YearMonth', 'Year', 'Month', 'Quarter',
                                     'Country', 'Feedback', 'Customer_Segment', 'Customer_ID', 'Product_Brand',
                                     'Product_Type', 'products', 'State', 'City', 'Income', 'Shipping_Method',
                                     'Payment_Method'])

def get_unique_sorted_values(df, column):
    """Safely get unique sorted values from a column, handling NaN values"""
    if column not in df.columns:
        return []
    
    # Get unique values and handle NaN
    unique_values = df[column].dropna().unique().tolist()
    
    # Convert all values to strings to avoid type comparison issues
    unique_values = [str(val) for val in unique_values]
    
    # Sort and return
    return sorted(unique_values)

def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #3366cc;
        text-align: center;
        margin-bottom: 20px;
    }
    .subheader {
        font-size: 24px;
        font-weight: bold;
        color: #5c5c5c;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #3366cc;
    }
    .metric-label {
        font-size: 16px;
        color: #5c5c5c;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">Retail Sales Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Check if data is loaded and not empty
    if df.empty:
        st.error("No data available. Please check your data file.")
        return
    
    # Create a sidebar for filters
    with st.sidebar:
        st.title("Filters")
        
        # Date range filter
        st.subheader("Date Range")
        if 'Date' in df.columns and not df['Date'].empty:
            min_date = df['Date'].min().date()
            max_date = df['Date'].max().date()
            date_range = st.date_input(
                "Select date range",
                [min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
            
            if len(date_range) == 2:
                start_date, end_date = date_range
                filtered_df = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
            else:
                filtered_df = df.copy()
        else:
            st.warning("Date column not available or empty")
            filtered_df = df.copy()
        
        # Category filter
        st.subheader("Product Category")
        if 'Product_Category' in df.columns:
            categories = ["All"] + get_unique_sorted_values(df, 'Product_Category')
            selected_category = st.selectbox("Select category", categories)
            
            if selected_category != "All":
                filtered_df = filtered_df[filtered_df['Product_Category'] == selected_category]
        
        # Country filter
        st.subheader("Country")
        if 'Country' in df.columns:
            countries = ["All"] + get_unique_sorted_values(df, 'Country')
            selected_country = st.selectbox("Select country", countries)
            
            if selected_country != "All":
                filtered_df = filtered_df[filtered_df['Country'] == selected_country]
        
        # Feedback filter
        st.subheader("Customer Feedback")
        if 'Feedback' in df.columns:
            feedbacks = ["All"] + get_unique_sorted_values(df, 'Feedback')
            selected_feedback = st.selectbox("Select feedback type", feedbacks)
            
            if selected_feedback != "All":
                filtered_df = filtered_df[filtered_df['Feedback'] == selected_feedback]
        
        # Customer segment filter
        st.subheader("Customer Segment")
        if 'Customer_Segment' in df.columns:
            segments = ["All"] + get_unique_sorted_values(df, 'Customer_Segment')
            selected_segment = st.selectbox("Select customer segment", segments)
            
            if selected_segment != "All":
                filtered_df = filtered_df[filtered_df['Customer_Segment'] == selected_segment]
    
    # Check if we have data after filtering
    if filtered_df.empty:
        st.error("No data available with the selected filters. Please adjust your selection.")
        return
    
    # Create metrics cards
    st.markdown('<div class="subheader">Key Metrics</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = filtered_df['Amount'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Sales</div>
            <div class="metric-value">${total_sales:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_order = filtered_df['Amount'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Order Value</div>
            <div class="metric-value">${avg_order:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if 'Customer_ID' in filtered_df.columns:
            total_customers = filtered_df['Customer_ID'].nunique()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Unique Customers</div>
                <div class="metric-value">{total_customers:,}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Unique Customers</div>
                <div class="metric-value">N/A</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        total_transactions = len(filtered_df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Transactions</div>
            <div class="metric-value">{total_transactions:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs for different analysis views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sales Trends", "Product Analysis", "Regional Analysis", "Customer Analysis", "Campaign Performance"])
    
    with tab1:
        st.markdown('<div class="subheader">Sales Trends Analysis</div>', unsafe_allow_html=True)
        
        # Time aggregation selection
        time_agg = st.radio(
            "Time Aggregation",
            options=["Monthly", "Quarterly", "Yearly"],
            horizontal=True
        )
        
        # Create time series chart based on selection
        try:
            if time_agg == "Monthly":
                sales_over_time = filtered_df.groupby('YearMonth', observed=True)['Amount'].sum().reset_index()
                sales_over_time = sales_over_time.sort_values('YearMonth')
                
                fig = px.line(
                    sales_over_time,
                    x='YearMonth',
                    y='Amount',
                    title="Monthly Sales Trend",
                    markers=True
                )
            elif time_agg == "Quarterly":
                sales_over_time = filtered_df.groupby(['Year', 'Quarter'], observed=True)['Amount'].sum().reset_index()
                sales_over_time['QuarterLabel'] = sales_over_time.apply(lambda x: f"{int(x['Year'])} Q{int(x['Quarter'])}", axis=1)
                sales_over_time = sales_over_time.sort_values(['Year', 'Quarter'])
                
                fig = px.line(
                    sales_over_time,
                    x='QuarterLabel',
                    y='Amount',
                    title="Quarterly Sales Trend",
                    markers=True
                )
            else:  # Yearly
                sales_over_time = filtered_df.groupby('Year', observed=True)['Amount'].sum().reset_index()
                sales_over_time = sales_over_time.sort_values('Year')
                
                fig = px.line(
                    sales_over_time,
                    x='Year',
                    y='Amount',
                    title="Yearly Sales Trend",
                    markers=True
                )
            
            fig.update_layout(
                xaxis_title="Time Period",
                yaxis_title="Sales Amount ($)",
                yaxis=dict(
                    tickformat="$,.0f"
                ),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Month-over-month growth rates
            if time_agg == "Monthly" and len(sales_over_time) > 1:
                st.subheader("Month-over-Month Growth Rate")
                
                sales_over_time['PrevMonth'] = sales_over_time['Amount'].shift(1)
                sales_over_time['Growth'] = (sales_over_time['Amount'] - sales_over_time['PrevMonth']) / sales_over_time['PrevMonth'] * 100
                sales_over_time = sales_over_time.dropna()
                
                fig = px.bar(
                    sales_over_time,
                    x='YearMonth',
                    y='Growth',
                    title="Monthly Growth Rate (%)",
                    color='Growth',
                    color_continuous_scale=["red", "green"],
                    color_continuous_midpoint=0
                )
                
                fig.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Growth Rate (%)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error generating sales trend charts: {e}")
    
    with tab2:
        st.markdown('<div class="subheader">Product Analysis</div>', unsafe_allow_html=True)
        
        try:
            col1, col2 = st.columns(2)
            
            with col1:
                # Product Category Performance
                if 'Product_Category' in filtered_df.columns:
                    category_sales = filtered_df.groupby('Product_Category', observed=True)['Amount'].sum().reset_index()
                    category_sales = category_sales.sort_values('Amount', ascending=False)
                    
                    fig = px.bar(
                        category_sales,
                        x='Product_Category',
                        y='Amount',
                        title="Sales by Product Category",
                        color='Amount',
                        color_continuous_scale=px.colors.sequential.Blues
                    )
                    
                    fig.update_layout(
                        xaxis_title="Product Category",
                        yaxis_title="Sales Amount ($)",
                        yaxis=dict(
                            tickformat="$,.0f"
                        ),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Product Category data not available")
            
            with col2:
                # Product Brand Performance
                if 'Product_Brand' in filtered_df.columns:
                    brand_sales = filtered_df.groupby('Product_Brand', observed=True)['Amount'].sum().reset_index()
                    brand_sales = brand_sales.sort_values('Amount', ascending=False).head(10)
                    
                    fig = px.pie(
                        brand_sales,
                        values='Amount',
                        names='Product_Brand',
                        title="Top 10 Product Brands by Sales",
                        hole=0.4
                    )
                    
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Product Brand data not available")
            
            # Product Type Analysis
            if 'Product_Type' in filtered_df.columns:
                product_type_sales = filtered_df.groupby('Product_Type')['Amount'].sum().reset_index()
                product_type_sales = product_type_sales.sort_values('Amount', ascending=False).head(10)
                
                fig = px.bar(
                    product_type_sales,
                    y='Product_Type',
                    x='Amount',
                    title="Sales by Product Type",
                    orientation='h',
                    color='Amount',
                    color_continuous_scale=px.colors.sequential.Viridis
                )
                
                fig.update_layout(
                    yaxis_title="Product Type",
                    xaxis_title="Sales Amount ($)",
                    xaxis=dict(
                        tickformat="$,.0f"
                    ),
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Individual products
            st.subheader("Top 10 Specific Products by Sales")
            product_sales = filtered_df.groupby('products')['Amount'].sum().reset_index()
            product_sales = product_sales.sort_values('Amount', ascending=False).head(10)
            
            fig = px.bar(
                product_sales,
                y='products',
                x='Amount',
                title="Top 10 Specific Products",
                orientation='h',
                color='Amount',
                color_continuous_scale=px.colors.sequential.Plasma
            )
            
            fig.update_layout(
                yaxis_title="Product",
                xaxis_title="Sales Amount ($)",
                xaxis=dict(
                    tickformat="$,.0f"
                ),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error generating product analysis charts: {e}")
    
    with tab3:
        st.markdown('<div class="subheader">Regional Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Country Performance
            country_sales = filtered_df.groupby('Country')['Amount'].sum().reset_index()
            country_sales = country_sales.sort_values('Amount', ascending=False)
            
            fig = px.bar(
                country_sales,
                x='Country',
                y='Amount',
                title="Sales by Country",
                color='Country'
            )
            
            fig.update_layout(
                xaxis_title="Country",
                yaxis_title="Sales Amount ($)",
                yaxis=dict(
                    tickformat="$,.0f"
                ),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # State/Region Performance
            state_sales = filtered_df.groupby('State')['Amount'].sum().reset_index()
            state_sales = state_sales.sort_values('Amount', ascending=False).head(10)
            
            fig = px.pie(
                state_sales,
                values='Amount',
                names='State',
                title="Top 10 States by Sales"
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # City Analysis
        st.subheader("Top 15 Cities by Sales")
        city_sales = filtered_df.groupby('City')['Amount'].sum().reset_index()
        city_sales = city_sales.sort_values('Amount', ascending=False).head(15)
        
        fig = px.bar(
            city_sales,
            y='City',
            x='Amount',
            title="Sales by City",
            orientation='h',
            color='Amount',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        fig.update_layout(
            yaxis_title="City",
            xaxis_title="Sales Amount ($)",
            xaxis=dict(
                tickformat="$,.0f"
            ),
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Create a geographic view if map data is available
        st.subheader("Geographic Sales Distribution")
        st.info("This is a placeholder for a geographic map. To implement a true geographic map, country codes or coordinates would be required.")
    
    with tab4:
        st.markdown('<div class="subheader">Customer Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Customer Segment Analysis
            segment_sales = filtered_df.groupby('Customer_Segment')['Amount'].sum().reset_index()
            
            fig = px.pie(
                segment_sales,
                values='Amount',
                names='Customer_Segment',
                title="Sales by Customer Segment",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Income Level Analysis
            income_sales = filtered_df.groupby('Income')['Amount'].sum().reset_index()
            
            fig = px.bar(
                income_sales,
                x='Income',
                y='Amount',
                title="Sales by Income Level",
                color='Income'
            )
            
            fig.update_layout(
                xaxis_title="Income Level",
                yaxis_title="Sales Amount ($)",
                yaxis=dict(
                    tickformat="$,.0f"
                ),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Order Value Distribution
        st.subheader("Customer Order Value Distribution")
        
        fig = px.histogram(
            filtered_df,
            x='Amount',
            nbins=50,
            title="Order Value Distribution",
            marginal="box"  # Add a box plot to the side
        )
        
        fig.update_layout(
            xaxis_title="Order Amount ($)",
            yaxis_title="Frequency",
            xaxis=dict(
                tickformat="$,.0f"
            ),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Customer Age Analysis
        if 'Age' in filtered_df.columns:
            st.subheader("Sales by Customer Age")
            
            # Create age bins for easier analysis
            filtered_df['Age_Group'] = pd.cut(
                filtered_df['Age'],
                bins=[0, 18, 25, 35, 45, 55, 65, 100],
                labels=['Under 18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
            )
            
            age_sales = filtered_df.groupby('Age_Group')['Amount'].sum().reset_index()
            
            fig = px.bar(
                age_sales,
                x='Age_Group',
                y='Amount',
                title="Sales by Age Group",
                color='Age_Group'
            )
            
            fig.update_layout(
                xaxis_title="Age Group",
                yaxis_title="Sales Amount ($)",
                yaxis=dict(
                    tickformat="$,.0f"
                ),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.markdown('<div class="subheader">Feedback & Marketing Performance</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Feedback Analysis
            feedback_sales = filtered_df.groupby('Feedback')['Amount'].agg(['sum', 'mean', 'count']).reset_index()
            feedback_sales = feedback_sales.rename(columns={'sum': 'Total_Sales', 'mean': 'Average_Order', 'count': 'Order_Count'})
            
            fig = px.bar(
                feedback_sales,
                x='Feedback',
                y='Total_Sales',
                title="Sales by Feedback Type",
                color='Feedback'
            )
            
            fig.update_layout(
                xaxis_title="Feedback",
                yaxis_title="Total Sales ($)",
                yaxis=dict(
                    tickformat="$,.0f"
                ),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Average Order Value by Feedback
            fig = px.bar(
                feedback_sales,
                x='Feedback',
                y='Average_Order',
                title="Average Order Value by Feedback",
                color='Feedback'
            )
            
            fig.update_layout(
                xaxis_title="Feedback",
                yaxis_title="Average Order Value ($)",
                yaxis=dict(
                    tickformat="$,.0f"
                ),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Scatter plot of Feedback vs. Order Count
        st.subheader("Feedback Impact Analysis")
        
        fig = px.scatter(
            feedback_sales,
            x='Feedback',
            y='Average_Order',
            size='Order_Count',
            color='Feedback',
            title="Feedback vs. Average Order Value (bubble size = order count)"
        )
        
        fig.update_layout(
            xaxis_title="Feedback Type",
            yaxis_title="Average Order Value ($)",
            yaxis=dict(
                tickformat="$,.0f"
            ),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Shipping Method Analysis
        st.subheader("Sales by Shipping Method")
        shipping_sales = filtered_df.groupby('Shipping_Method')['Amount'].sum().reset_index()
        
        fig = px.pie(
            shipping_sales,
            values='Amount',
            names='Shipping_Method',
            title="Sales by Shipping Method",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Payment Method Analysis
        st.subheader("Sales by Payment Method")
        payment_sales = filtered_df.groupby('Payment_Method')['Amount'].sum().reset_index()
        
        fig = px.bar(
            payment_sales,
            x='Payment_Method',
            y='Amount',
            title="Sales by Payment Method",
            color='Payment_Method'
        )
        
        fig.update_layout(
            xaxis_title="Payment Method",
            yaxis_title="Sales Amount ($)",
            yaxis=dict(
                tickformat="$,.0f"
            ),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Add a data explorer for advanced users
    st.markdown('<div class="subheader">Data Explorer</div>', unsafe_allow_html=True)
    st.write("Explore the data directly by selecting columns to display:")
    
    # Allow users to select columns
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect("Select columns to view", all_columns, default=all_columns[:10])
    
    if selected_columns:
        st.dataframe(filtered_df[selected_columns].head(100))
    
    # Download option
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_retail_data.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    main()