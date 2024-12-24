import pandas as pd
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# Establish connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",  # Change this if your PostgreSQL is on a different server
    database="xdr_data_db",  # Replace with your actual database name
    user="postgres",  # Replace with your PostgreSQL username
    password="8128"  # Replace with your PostgreSQL password
)

# SQL query to extract data from your table
query = "SELECT * FROM xdr_data;"  # Replace 'xdr_table' with your actual table name

# Use pandas to read the SQL query results into a DataFrame
df = pd.read_sql(query, conn)

# Save the data to a CSV file
df.to_csv("data/raw_data.csv", index=False)

# Print a message indicating the extraction is complete
print("Data extraction complete!")




# Assuming `conn` is your database connection
query = """
SELECT 
    "MSISDN/Number" AS MSISDN, 
    COUNT("Bearer Id") AS xdr_sessions,
    SUM("Dur. (ms)") / 1000 AS total_duration, -- Convert ms to seconds
    SUM("Total DL (Bytes)") AS total_dl,
    SUM("Total UL (Bytes)") AS total_ul,
    SUM("Total DL (Bytes)" + "Total UL (Bytes)") AS total_data
FROM xdr_data
GROUP BY "MSISDN/Number";
"""
data = pd.read_sql_query(query, conn)

# Step 3: Treat Missing Values and Outliers
data.fillna(data.mean(), inplace=True)

# Detect and treat outliers (Cap values to 95th percentile)
for col in ['total_duration', 'total_dl', 'total_ul', 'total_data']:
    upper_limit = data[col].quantile(0.95)
    data[col] = data[col].clip(upper=upper_limit)

# Step 4: Segment Users into Decile Classes
data['duration_decile'] = pd.qcut(data['total_duration'], 10, labels=False)
decile_data = data.groupby('duration_decile').agg({'total_data': 'sum'}).reset_index()

# Step 5: Univariate and Bivariate Analysis
# Example: Scatter plot for bivariate analysis
sns.scatterplot(data=data, x='total_dl', y='total_ul')
plt.show()

# Step 6: Correlation Analysis
correlation_matrix = data[['total_dl', 'total_ul', 'total_data']].corr()
sns.heatmap(correlation_matrix, annot=True)
plt.show()

# Step 7: Dimensionality Reduction using PCA
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data[['total_dl', 'total_ul', 'total_data']])

# PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_data)

print("Explained Variance Ratio:", pca.explained_variance_ratio_)