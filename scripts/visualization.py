import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load aggregated customer data
customer_data = pd.read_csv('aggregated_customer_data.csv')

# Create a directory to save the plots if it doesn't exist
output_dir = 'visualizations'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Distribution of average throughput per handset type
plt.figure(figsize=(12, 6))
sns.boxplot(x='Handset Type', y='avg_tp_dl', data=customer_data)
plt.xticks(rotation=90)
plt.title("Distribution of Average Throughput per Handset Type")
plt.ylabel("Average Throughput (kbps)")

# Save the box plot as a PNG image
boxplot_file = os.path.join(output_dir, 'avg_throughput_per_handset_type.png')
plt.savefig(boxplot_file, bbox_inches='tight')  # bbox_inches='tight' ensures the title and labels fit
plt.close()  # Close the plot to avoid overlap

print(f"Box plot saved as: {boxplot_file}")

# Bar plot for average TCP retransmissions per handset type
avg_tcp_by_handset = customer_data.groupby('Handset Type')['avg_tcp_dl_retrans'].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(x='Handset Type', y='avg_tcp_dl_retrans', data=avg_tcp_by_handset)
plt.xticks(rotation=90)
plt.title("Average TCP Retransmission per Handset Type")
plt.ylabel("Average TCP DL Retransmission (Bytes)")

# Save the bar plot as a PNG image
barplot_file = os.path.join(output_dir, 'avg_tcp_retransmission_per_handset_type.png')
plt.savefig(barplot_file, bbox_inches='tight')
plt.close()  # Close the plot

print(f"Bar plot saved as: {barplot_file}")
