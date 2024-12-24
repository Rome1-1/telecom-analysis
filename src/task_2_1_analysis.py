import psycopg2
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Database connection details
conn = psycopg2.connect(
    host="localhost",  # Change this if your PostgreSQL is on a different server
    database="xdr_data_db",  # Replace with your actual database name
    user="postgres",  # Replace with your PostgreSQL username
    password="8128"  # Replace with your PostgreSQL password
)

# Updated SQL query with correct column names
query = """
    SELECT
        "MSISDN/Number",  -- Correct column name
        "Dur. (ms)",      -- Correct column name for total duration
        "Total DL (Bytes)",  -- Correct column name for total download bytes
        "Total UL (Bytes)",  -- Correct column name for total upload bytes
        "Social Media DL (Bytes)",
        "Google DL (Bytes)",
        "Email DL (Bytes)",
        "Youtube DL (Bytes)",
        "Netflix DL (Bytes)",
        "Gaming DL (Bytes)",
        "Other DL (Bytes)"
    FROM xdr_data
"""

# Load data from PostgreSQL database
data = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Check the first few rows of the data to confirm successful loading
print(data.head())

# Define the features for clustering (ensure to use the correct column names)
features = [
    "Dur. (ms)",  # Total duration
    "Total DL (Bytes)",
    "Total UL (Bytes)",
    "Social Media DL (Bytes)",
    "Google DL (Bytes)",
    "Email DL (Bytes)",
    "Youtube DL (Bytes)",
    "Netflix DL (Bytes)",
    "Gaming DL (Bytes)",
    "Other DL (Bytes)"
]

# Ensure no missing data before proceeding (drop rows with any NaN values)
data_cleaned = data[features].dropna()

# Normalize the data using StandardScaler
scaler = StandardScaler()
normalized_data = scaler.fit_transform(data_cleaned)

# Apply K-Means clustering with k=3
kmeans = KMeans(n_clusters=3, random_state=42)
data_cleaned['cluster'] = kmeans.fit_predict(normalized_data)

# Add the cluster column to the original dataframe
data['cluster'] = data_cleaned['cluster']

# Check the first few rows with cluster assignments
print(data[['MSISDN/Number', 'cluster']].head())

# Plot the clusters (using 'Total DL (Bytes)' and 'Total UL (Bytes)' for visualization)
plt.scatter(data_cleaned['Total DL (Bytes)'], data_cleaned['Total UL (Bytes)'], c=data_cleaned['cluster'], cmap='viridis')
plt.xlabel('Total DL (Bytes)')
plt.ylabel('Total UL (Bytes)')
plt.title('Clustering of XDR Data')
plt.show()

# Compute statistics for each cluster
cluster_stats = data.groupby('cluster').agg({
    'Dur. (ms)': ['min', 'max', 'mean', 'sum'],
    'Total DL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Total UL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Social Media DL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Google DL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Email DL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Youtube DL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Netflix DL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Gaming DL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Other DL (Bytes)': ['min', 'max', 'mean', 'sum']
}).reset_index()

# Display cluster statistics
print(cluster_stats)

# Aggregate total traffic per application (DL + UL)
app_data = data[['MSISDN/Number', 'Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)', 
                 'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']]

# Sum traffic per application
app_totals = app_data.sum(axis=0).reset_index(name='total_data')
app_totals.columns = ['application', 'total_data']

# Sort and get the top 10 most engaged users per application
top_app_users = app_totals.sort_values(by='total_data', ascending=False).head(10)
print(top_app_users)

# Plot the top 3 most used applications
top_3_apps = app_totals.sort_values(by='total_data', ascending=False).head(3)
sns.barplot(x='total_data', y='application', data=top_3_apps)
plt.title('Top 3 Most Used Applications')
plt.show()

# Use the elbow method to find the optimal number of clusters
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(normalized_data)
    inertia.append(kmeans.inertia_)

# Plot the elbow curve
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.show()

# Plot the clusters (using 'Total DL (Bytes)' and 'Total UL (Bytes)' for visualization)
plt.scatter(data_cleaned['Total DL (Bytes)'], data_cleaned['Total UL (Bytes)'], c=data_cleaned['cluster'], cmap='viridis')
plt.xlabel('Total DL (Bytes)')
plt.ylabel('Total UL (Bytes)')
plt.title('Clustering of XDR Data')

# Save the plot as an image
plt.savefig('clustering_plot.png')  # Save as PNG file
plt.show()

# Plot the elbow method for optimal k
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')

# Save the elbow plot as an image
plt.savefig('elbow_method_plot.png')
plt.show()
