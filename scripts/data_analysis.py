# Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import mstats

# Load the data
df = pd.read_csv(r'C:\Users\teble\telecom-analysis\notebooks\Copy of Week2_challenge_data_source(CSV).csv')

# Check the column names to ensure 'user_id' exists
print(df.columns)

# Strip spaces from column names (if there are any)
df.columns = df.columns.str.strip()

# Aggregate data using 'IMSI' as the user identifier
user_sessions = df.groupby('IMSI')['MSISDN/Number'].count().rename('xDR_sessions')  # Using MSISDN/Number as session ID
user_duration = df.groupby('IMSI')['Dur. (ms)'].sum().rename('total_session_duration')  # Assuming 'Dur. (ms)' is the session duration
user_dl = df.groupby('IMSI')['Total DL (Bytes)'].sum().rename('total_download_data')  # Assuming 'Total DL (Bytes)' is total DL data
user_ul = df.groupby('IMSI')['Total UL (Bytes)'].sum().rename('total_upload_data')  # Assuming 'Total UL (Bytes)' is total UL data
user_data_volume = (user_dl + user_ul).rename('total_data_volume')

# Combine aggregated data
user_data = pd.concat([user_sessions, user_duration, user_dl, user_ul, user_data_volume], axis=1)

# Save the aggregated data to a CSV
user_data.to_csv('aggregated_user_data.csv')

# Load the aggregated data
user_data = pd.read_csv('aggregated_user_data.csv')

# Handle missing values
user_data.fillna(user_data.mean(), inplace=True)

# Optional: Winsorize or handle outliers
user_data['total_session_duration'] = mstats.winsorize(user_data['total_session_duration'], limits=[0.05, 0.05])

# Segment users into deciles based on total session duration
user_data['duration_decile'] = pd.qcut(user_data['total_session_duration'], 10, labels=False)
decile_data = user_data.groupby('duration_decile')['total_data_volume'].sum()

# Print basic descriptive statistics
print(user_data.describe())

# Univariate analysis: Histogram, Boxplot, and KDE for 'total_session_duration'
sns.histplot(user_data['total_session_duration'])
plt.show()

sns.boxplot(x=user_data['total_session_duration'])
plt.show()

sns.kdeplot(user_data['total_session_duration'])
plt.show()

# Correlation matrix
correlation_matrix = user_data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.show()

# PCA for dimensionality reduction
scaler = StandardScaler()
scaled_data = scaler.fit_transform(user_data.select_dtypes(include=['float64', 'int64']))
pca = PCA(n_components=2)
principal_components = pca.fit_transform(scaled_data)
print(pca.explained_variance_ratio_)

# Example: Save graph as PNG file
sns.histplot(user_data['total_session_duration'])
plt.savefig('total_session_duration_histogram.png')  # Save as image file
plt.close()  # Close the plot after saving it

sns.boxplot(x=user_data['total_session_duration'])
plt.savefig('total_session_duration_boxplot.png')  # Save as image file
plt.close()  # Close the plot after saving it

sns.kdeplot(user_data['total_session_duration'])
plt.savefig('total_session_duration_kdeplot.png')  # Save as image file
plt.close()  # Close the plot after saving it
