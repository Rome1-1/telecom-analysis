import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Create SQLAlchemy engine using psycopg2
engine = create_engine('postgresql+psycopg2://postgres:8128@localhost:5432/xdr_data_db')

# Load data into a DataFrame
query = "SELECT * FROM xdr_data;"
df = pd.read_sql(query, engine)

# Print out the shape of the dataframe (number of rows and columns)
print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Replace missing numeric values with the column mean
numeric_cols = ['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 
                'Avg RTT DL (ms)', 'Avg RTT UL (ms)', 
                'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']
for col in numeric_cols:
    missing_count_before = df[col].isna().sum()
    df[col] = df[col].fillna(df[col].mean())
    missing_count_after = df[col].isna().sum()
    print(f"Column '{col}': {missing_count_before} missing values before, {missing_count_after} missing values after.")

# Replace missing categorical values with the mode
missing_handset_before = df['Handset Type'].isna().sum()
df['Handset Type'] = df['Handset Type'].fillna(df['Handset Type'].mode()[0])
missing_handset_after = df['Handset Type'].isna().sum()
print(f"Handset Type: {missing_handset_before} missing values before, {missing_handset_after} missing values after.")

# Remove Outliers using IQR
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Clip the data to remove the outliers
    df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
    print(f"Outliers removed for column '{col}' based on IQR.")

# Optionally, save the cleaned data to a new CSV file
df.to_csv('cleaned_data.csv', index=False)
print("Cleaned data saved to 'cleaned_data.csv'.")

# Close the connection
engine.dispose()
print("Database connection closed.")
