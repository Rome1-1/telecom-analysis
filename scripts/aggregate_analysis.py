# aggregate_analysis.py
import pandas as pd

# Load the cleaned data
df = pd.read_csv('cleaned_data.csv')

# Aggregate metrics per customer
customer_data = df.groupby('MSISDN/Number').agg({
    'TCP DL Retrans. Vol (Bytes)': 'mean',
    'TCP UL Retrans. Vol (Bytes)': 'mean',
    'Avg RTT DL (ms)': 'mean',
    'Avg RTT UL (ms)': 'mean',
    'Avg Bearer TP DL (kbps)': 'mean',
    'Avg Bearer TP UL (kbps)': 'mean',
    'Handset Type': 'max'
}).reset_index()

# Rename columns for clarity
customer_data.rename(columns={
    'TCP DL Retrans. Vol (Bytes)': 'avg_tcp_dl_retrans',
    'TCP UL Retrans. Vol (Bytes)': 'avg_tcp_ul_retrans',
    'Avg RTT DL (ms)': 'avg_rtt_dl',
    'Avg RTT UL (ms)': 'avg_rtt_ul',
    'Avg Bearer TP DL (kbps)': 'avg_tp_dl',
    'Avg Bearer TP UL (kbps)': 'avg_tp_ul',
}, inplace=True)

# Top 10, Bottom 10, and Most Frequent TCP DL Retransmissions
print("Top 10 TCP DL Retransmissions:")
print(customer_data['avg_tcp_dl_retrans'].nlargest(10))

print("Bottom 10 TCP DL Retransmissions:")
print(customer_data['avg_tcp_dl_retrans'].nsmallest(10))

print("Most Frequent TCP DL Retransmissions:")
print(customer_data['avg_tcp_dl_retrans'].value_counts().head(10))

# Save the aggregated customer data
customer_data.to_csv('aggregated_customer_data.csv', index=False)
