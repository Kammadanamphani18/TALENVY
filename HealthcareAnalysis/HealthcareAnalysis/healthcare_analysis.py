import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

st.set_page_config(layout="wide")
st.title("🩺 Healthcare Analytics Dashboard")

# Sidebar for file upload
uploaded_file = st.sidebar.file_uploader("📁 Upload your Healthcare CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Display dataset information
    st.subheader("📊 Dataset Overview")
    st.write(f"**Shape of dataset:** {df.shape}")
    st.write("**First 5 rows:**")
    st.dataframe(df.head())

    # Identify target column
    target_column = st.selectbox("🎯 Select the target column for prediction", options=df.columns)

    # Check for missing values
    st.subheader("🔍 Missing Values")
    missing_values = df.isnull().sum()
    st.write(missing_values[missing_values > 0])

    # Visualize distribution of target variable
    st.subheader("📈 Target Variable Distribution")
    fig, ax = plt.subplots()
    df[target_column].value_counts().plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # Correlation heatmap
    st.subheader("📊 Correlation Heatmap")
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    fig2, ax2 = plt.subplots(figsize=(10,8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax2)
    st.pyplot(fig2)

    # Prepare data for modeling
    st.subheader("🤖 Model Training")
    features = st.multiselect("Select features for model training", options=[col for col in df.columns if col != target_column])

    if features:
        X = df[features]
        y = df[target_column]

        # Handle categorical variables
        X = pd.get_dummies(X, drop_first=True)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Display accuracy
        accuracy = accuracy_score(y_test, y_pred)
        st.write(f"**Model Accuracy:** {accuracy:.2f}")

        # Feature importance
        st.subheader("📌 Feature Importance")
        importance = pd.Series(model.coef_[0], index=X.columns)
        fig3, ax3 = plt.subplots()
        importance.sort_values().plot(kind='barh', ax=ax3)
        st.pyplot(fig3)

        # User input for prediction
        st.subheader("🔎 Make a Prediction")
        user_input = {}
        for feature in features:
            value = st.text_input(f"Enter value for {feature}")
            user_input[feature] = value

        if st.button("Predict"):
            input_df = pd.DataFrame([user_input])
            input_df = pd.get_dummies(input_df)
            input_df = input_df.reindex(columns=X.columns, fill_value=0)
            prediction = model.predict(input_df)[0]
            st.write(f"**Predicted {target_column}:** {prediction}")
    else:
        st.warning("Please select at least one feature for model training.")
else:
    st.info("Please upload a CSV file to begin analysis.")
