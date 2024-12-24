import pandas as pd
import streamlit as st

# Load the dataset
data_path = 'C:/Users/teble/telecom-analysis/data/raw_data.csv'  # Update with the correct data path
df = pd.read_csv(data_path)

# Check the columns in the dataframe to ensure the 'Cluster' column exists
st.write("Columns in the dataframe:", df.columns)

# Make sure the 'Cluster' column exists before proceeding
if 'Cluster' in df.columns:
    # Get the counts of each cluster
    cluster_counts = df['Cluster'].value_counts()
    st.write("Cluster Distribution:")
    st.write(cluster_counts)
else:
    st.error("The 'Cluster' column does not exist in the dataset. Please check the data.")

# Example of further analysis: showing summary statistics for numeric columns
st.write("Summary Statistics:")
st.write(df.describe())

# Example of engagement and experience analysis (if these columns exist in your dataset)
if 'Engagement' in df.columns and 'Experience' in df.columns:
    st.write("Engagement vs Experience Scatter Plot:")
    st.scatter_chart(df[['Engagement', 'Experience']])

# Handle other analyses as needed (like satisfaction score, etc.)
# For example, if 'Satisfaction' is a column in the dataset:
if 'Satisfaction' in df.columns:
    st.write("Satisfaction Score Distribution:")
    st.bar_chart(df['Satisfaction'].value_counts())

# Example: Showing correlation heatmap if there are numerical features
import seaborn as sns
import matplotlib.pyplot as plt

# Check for numerical columns
numeric_columns = df.select_dtypes(include=['number']).columns
if len(numeric_columns) > 1:
    st.write("Correlation Heatmap:")
    correlation_matrix = df[numeric_columns].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    st.pyplot(plt)

# Handle missing data: Show the percentage of missing data
st.write("Missing Data Percentage:")
missing_data_percentage = df.isnull().mean() * 100
st.write(missing_data_percentage)

# Handle outliers: Show box plots for numeric columns
if len(numeric_columns) > 0:
    st.write("Box Plots for Numeric Columns:")
    for col in numeric_columns:
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=df[col])
        plt.title(f"Box Plot for {col}")
        st.pyplot(plt)

# Streamlit needs to run with the `streamlit run` command, not python directly
st.write("To view the app, please run this file using the following command:")
st.write("`streamlit run C:/Users/teble/telecom-analysis/scripts/dashboard.py`")
# Local URL: http://localhost:8501
