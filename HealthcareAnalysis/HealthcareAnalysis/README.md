
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

## 🙋‍♂️ Author

**Sai Kiran**  
For queries or suggestions, feel free to contact me.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
