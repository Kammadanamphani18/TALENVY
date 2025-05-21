# TALENVY 


# 🩺 Healthcare Analytics Dashboard

A user-friendly web application built using **Streamlit** to perform interactive data analysis, visualization, and prediction on healthcare datasets. This tool enables users to upload their own healthcare-related CSV files, train models, evaluate outcomes, and gain valuable insights into patient health and hospital operations.

---

## 📌 Features

✅ Upload and preview your healthcare dataset  
✅ Automatically detect missing values and summarize key statistics  
✅ Visualize target variable distribution and feature correlations  
✅ Select features and train a logistic regression model  
✅ Get accuracy score and visualize feature importance  
✅ Make real-time predictions based on user input  
✅ Fully interactive and designed for large datasets  

---

## 📂 Example Compatible Datasets

You can upload any CSV file with relevant healthcare data. Below are a few recommended datasets:

| Dataset                              | Target Column  | Download Link                                                                 |
|-------------------------------------|----------------|--------------------------------------------------------------------------------|
| Diabetes Prediction Dataset         | `Outcome`      | [Kaggle Link](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database) |
| Heart Disease Dataset               | `target`       | [Kaggle Link](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset)     |
| Cardiovascular Disease Dataset      | `cardio`       | [Kaggle Link](https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset) |
| Mental Health Survey                | `treatment`    | [Kaggle Link](https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey)      |
| Medical Cost Dataset (Regression)   | `charges`      | [Kaggle Link](https://www.kaggle.com/datasets/mirichoi0218/insurance)                |

---

## 🚀 Getting Started

### 🔧 Prerequisites

Install Python (version 3.8+ recommended). Then, install required packages:

```bash
pip install streamlit pandas matplotlib seaborn scikit-learn
```

### 🛠️ Running the App

1. Clone the repository or download the `app.py` file.
2. Start the app using:

```bash
streamlit run app.py
```

3. Upload any of the datasets mentioned above via the sidebar and start exploring!

---

## 📊 Example Visualizations

- Glucose level distribution (histogram)
- Feature correlation matrix (heatmap)
- Feature impact (horizontal bar chart)
- Model performance (accuracy score)
- Pie charts for class distribution

---

## 📁 Project Structure

```
healthcare-dashboard/
│
├── app.py               # Main Streamlit app
├── README.md            # Project documentation
├── requirements.txt     # Python package dependencies (optional)
└── datasets/            # (Optional) Store sample CSV files here
```

---

## 🧠 Future Enhancements

- Add support for regression and classification models
- Integrate model comparison (Random Forest, SVM, etc.)
- Enable downloading model reports
- Improve UI/UX with custom themes
- Deploy using Streamlit Cloud or Heroku

---

## Reports


![Image](https://github.com/user-attachments/assets/84777554-9762-471f-bf09-07bfc51f47b3)

![Image](https://github.com/user-attachments/assets/5c906c13-d384-472d-9ef4-f2ce83bac14e)

![Image](https://github.com/user-attachments/assets/82c337fa-63e1-4c2b-91ac-a8c24896ce9c)

![Image](https://github.com/user-attachments/assets/f470fd92-41da-4248-b6e6-7f5421bfecea)

![Image](https://github.com/user-attachments/assets/dcc60629-5412-40eb-936b-66c5b2711762)

## 🙋‍♂️ Author

** Phanindra **  
For queries or suggestions, feel free to contact me.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



# Sales Performance Analysis Tool

This repository contains a comprehensive sales performance analysis toolkit designed to help businesses gain insights from their retail sales data. The toolkit includes data cleaning, analysis, visualization, and interactive dashboard capabilities.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Data Preparation](#data-preparation)
  - [Basic Analysis](#basic-analysis)
  - [Enhanced Analysis](#enhanced-analysis)
  - [Interactive Dashboard](#interactive-dashboard)
- [Example Outputs](#example-outputs)
- [Dependencies](#dependencies)
- [License](#license)

## Overview

The Sales Performance Analysis toolkit provides a suite of tools for analyzing retail sales data. It enables users to clean and prepare data, perform various analyses, generate visualizations, and create interactive dashboards. The toolkit is designed to be flexible, supporting data from both CSV/Excel files and SQL databases.

## Features

- **Data Cleaning**: Automated data cleaning including handling missing values, correcting data types, and removing outliers
- **Basic Sales Analysis**: Monthly trends, product category analysis, regional analysis, and marketing campaign impact
- **Enhanced Analysis**: Advanced metrics, shipping interval analysis, sales channel analysis, and time-based comparisons
- **Visualization**: Comprehensive charts and graphs for all analyses
- **Interactive Dashboard**: Streamlit-based interactive dashboard with filtering capabilities
- **SQL Integration**: Support for loading data directly from SQL databases
- **Report Generation**: Automated comprehensive report generation in Excel format

## Project Structure

```
SalesPerformanceAnalysis/
├── data/
│   ├── sales_data.csv
│   ├── new_retail_data.csv
│   └── new_retail_data_cleaned.csv
├── scripts/
│   ├── analyze_new_retail_data.py
│   ├── clean_retail_data.py
│   ├── create_sales_dashboard.py
│   ├── enhanced_sales_analysis.py
│   ├── generate_sample_data.py
│   ├── interactive_dashboard.py
│   ├── run_analysis.py
│   ├── sales_analysis.py
│   └── sql_analysis_example.py
├── reports/
│   ├── monthly_sales_trend.png
│   ├── top_product_categories.png
│   ├── regional_sales_distribution.png
│   ├── marketing_campaign_impact.png
│   └── sales_analysis_report.xlsx
└── sales_dashboard/
    ├── sales_dashboard.png
    ├── monthly_trend.png
    ├── top_products.png
    ├── feedback_impact.png
    └── customer_segment.png
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SalesPerformanceAnalysis.git
cd SalesPerformanceAnalysis
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Data Preparation

1. **Generate Sample Data** (if you don't have your own data):
```bash
python scripts/generate_sample_data.py
```

2. **Clean Retail Data**:
```bash
python scripts/clean_retail_data.py
```

### Basic Analysis

Run the basic sales performance analysis:

```bash
python scripts/run_analysis.py
```

This will generate several visualizations and a comprehensive Excel report in the `reports/` directory.

### Enhanced Analysis

For more advanced analysis:

```bash
python scripts/analyze_new_retail_data.py
```

### Interactive Dashboard

Launch the interactive Streamlit dashboard:

```bash
streamlit run scripts/interactive_dashboard.py
```

### SQL Analysis

To analyze data from a SQL database, modify the connection string in `scripts/sql_analysis_example.py` and run:

```bash
python scripts/sql_analysis_example.py
```

## Example Outputs

### Monthly Sales Trend
![Monthly Sales Trend](reports/monthly_sales_trend.png)

### Product Category Analysis
![Product Category Analysis](reports/top_product_categories.png)

### Regional Sales Distribution
![Regional Sales Distribution](reports/regional_sales_distribution.png)

### Marketing Campaign Impact
![Marketing Campaign Impact](reports/marketing_campaign_impact.png)

### Sales Dashboard
![Sales Dashboard](sales_dashboard/sales_dashboard.png)

## Dependencies

- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn
- sqlalchemy
- streamlit
- plotly
- scipy
- openpyxl

## Core Components

### SalesPerformanceAnalysis Class

The main analysis class that provides methods for:
- Loading data from files or SQL databases
- Analyzing monthly sales trends
- Analyzing product categories
- Analyzing regional sales performance
- Measuring marketing campaign impact
- Generating comprehensive reports

```python
# Example usage
from sales_analysis import SalesPerformanceAnalysis

analyzer = SalesPerformanceAnalysis(data_source="data/sales_data.csv")
analyzer.load_data_from_file()
analyzer.monthly_sales_trend()
analyzer.product_category_analysis()
analyzer.regional_sales_analysis()
analyzer.marketing_campaign_impact()
analyzer.generate_comprehensive_report()
```

### EnhancedSalesAnalysis Class

Extends the basic analysis with more advanced features:
- Key business metrics calculation
- Shipping interval analysis
- Sales channel analysis
- Monthly/quarterly comparisons

```python
# Example usage
from enhanced_sales_analysis import EnhancedSalesAnalysis

enhanced_analyzer = EnhancedSalesAnalysis(data_source="data/sales_data.csv")
metrics = enhanced_analyzer.calculate_key_metrics()
enhanced_analyzer.shipping_interval_analysis()
enhanced_analyzer.sales_by_channel()
enhanced_analyzer.monthly_quarterly_analysis(period='monthly')
```

### Interactive Dashboard

A Streamlit-based interactive dashboard with:
- Dynamic filtering capabilities
- Multiple analysis tabs
- Downloadable filtered data
- Interactive visualizations

## Reports
![Image](https://github.com/user-attachments/assets/fc8acb69-24ba-4514-969b-b6982eebe4b2)

![Image](https://github.com/user-attachments/assets/330e2df9-b48b-43b8-b78f-0bd898da3f7b)

![Image](https://github.com/user-attachments/assets/c6a8e073-156c-4e4d-b189-a5fc8f1daa4d)

![Image](https://github.com/user-attachments/assets/ace6bbdf-321b-4c23-acbd-d2e99b711040)

![Image](https://github.com/user-attachments/assets/6e0fee05-d08b-411f-961a-b681c1993044)

## License

This project is licensed under the MIT License - see the LICENSE file for details.



# Social Media Sentiment Analyzer

A web application that analyzes sentiment from Reddit comments about products/services using NLP and Flask.

![Main Interface](https://via.placeholder.com/800x500.png?text=Sentiment+Analysis+Input+Form)
![Results Page](https://via.placeholder.com/800x500.png?text=Sentiment+Distribution+Chart+and+Stats)

## Features

- Real-time Reddit comment analysis
- Sentiment classification (Positive/Negative/Neutral)
- Interactive pie chart visualization
- Mobile-responsive design
- User-friendly web interface
- Percentage-based sentiment breakdown

## Technologies Used

- **Python 3**
- **Flask** (Web Framework)
- **PRAW** (Reddit API Wrapper)
- **NLTK** (Natural Language Toolkit)
- **Plotly** (Data Visualization)
- **Bootstrap 5** (Frontend Design)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sentiment-analysis-project.git
cd sentiment-analysis-project
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Reddit API**
- Create `config.ini` in project root:
```ini
[REDDIT]
client_id = your_reddit_client_id
client_secret = your_reddit_client_secret
user_agent = sentiment_analysis_v1
```

## Usage

1. **Run the application**
```bash
python run.py
```

2. **Access the web interface**
```
http://localhost:5000
```

3. **Input parameters**
- Subreddit name (e.g., `technology`)
- Product/brand name (e.g., `iPhone`)
- Number of posts to analyze (default: 50)

## Project Structure

```
sentiment-analysis-project/
├── app/
│   ├── static/       # CSS files
│   ├── templates/    # HTML templates
│   ├── __init__.py
│   ├── reddit_api.py # Reddit API handler
│   └── sentiment_analysis.py # NLP processing
├── config.ini        # API credentials
├── requirements.txt  # Dependencies
└── run.py            # Application entry point
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Reports

![Image](https://github.com/user-attachments/assets/3f0450c4-df3e-4181-ba02-2d697d98a665)

![Image](https://github.com/user-attachments/assets/c6968158-8743-40ee-ad5b-9a9abec8dbd7)

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Support

For issues/questions, please [file an issue](https://github.com/yourusername/sentiment-analysis-project/issues).

---

**Note**: Replace placeholder images with actual screenshots:
1. Take screenshots of your running application
2. Upload to project's `/docs/images` folder
3. Update image URLs in this README
