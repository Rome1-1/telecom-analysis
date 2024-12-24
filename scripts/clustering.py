import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

# Load aggregated customer data
customer_data = pd.read_csv('aggregated_customer_data.csv')

# Select features for clustering
features = ['avg_tcp_dl_retrans', 'avg_rtt_dl', 'avg_tp_dl']
scaler = StandardScaler()
scaled_features = scaler.fit_transform(customer_data[features])

# Create a directory to save the plots if it doesn't exist
output_dir = 'visualizations'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Elbow method to determine optimal k
inertia = []
for k in range(1, 10):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_features)
    inertia.append(kmeans.inertia_)

# Plot Elbow Curve
plt.figure(figsize=(8, 5))
plt.plot(range(1, 10), inertia, marker='o')
plt.title("Elbow Method")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")

# Save Elbow Curve plot
elbow_curve_file = os.path.join(output_dir, 'elbow_method.png')
plt.savefig(elbow_curve_file, bbox_inches='tight')
plt.close()  # Close the plot
print(f"Elbow Method plot saved as: {elbow_curve_file}")

# Apply K-Means with k=3
kmeans = KMeans(n_clusters=3, random_state=42)
customer_data['cluster'] = kmeans.fit_predict(scaled_features)

# Analyze clusters
cluster_summary = customer_data.groupby('cluster')[features].agg(['min', 'max', 'mean', 'sum'])
print(cluster_summary)

# Visualize Clusters
sns.pairplot(customer_data, hue='cluster', vars=features)
plt.title("K-Means Clustering of Customers")

# Save Pairplot of Clusters
pairplot_file = os.path.join(output_dir, 'kmeans_clustering_pairplot.png')
plt.savefig(pairplot_file, bbox_inches='tight')
plt.close()  # Close the plot
print(f"K-Means Clustering pairplot saved as: {pairplot_file}")
