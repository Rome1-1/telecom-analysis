# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Step 1: Load the data (CSV file containing telecom data)
# Ensure the path to the CSV is correct
df = pd.read_csv(r'C:\Users\teble\telecom-analysis\notebooks\Copy of Week2_challenge_data_source(CSV).csv')



# Step 2: Set the title of the app
st.title("Telecom User Overview")

# Step 3: Display the first few rows of the dataframe
st.dataframe(df.head())

# Add a sidebar for filtering data (optional)
st.sidebar.title("Filter Options")

# Example of filtering by 'Handset Manufacturer' and 'Handset Type' (you can adjust the columns as per your data)
handset_manufacturer = st.sidebar.selectbox("Select Handset Manufacturer", df['Handset Manufacturer'].unique())
handset_type = st.sidebar.selectbox("Select Handset Type", df['Handset Type'].unique())

# Filter the dataframe based on the user's selections
filtered_data = df[(df['Handset Manufacturer'] == handset_manufacturer) & 
                   (df['Handset Type'] == handset_type)]

# Display the filtered data
st.subheader(f"Filtered Data: {handset_manufacturer} - {handset_type}")
st.dataframe(filtered_data)

# Example: Display a basic chart (e.g., Handset Manufacturer distribution)
st.subheader("Distribution of Handset Manufacturers")
st.bar_chart(df['Handset Manufacturer'].value_counts())

# Example: Show a line chart for average RTT Downlink (you can customize this based on your columns)
st.subheader("Average RTT Downlink Over Time")
df['Start'] = pd.to_datetime(df['Start'])  # Ensure the 'Start' column is in datetime format
df.set_index('Start', inplace=True)  # Set the index as the 'Start' datetime column
st.line_chart(df['Avg RTT DL (ms)'].resample('D').mean())  # Resample by day and plot


# Load your dataset
df = pd.read_csv(r'C:\Users\teble\telecom-analysis\notebooks\Copy of Week2_challenge_data_source(CSV).csv')

# Create a line chart for Avg RTT UL (ms)
st.title("Telecom User Overview")
 
# Sample data (replace this with your actual dataframe)
data = {
    'Start': ['2024-01-01', '2024-01-05', '2024-01-10', 'invalid_date'],
    'Avg RTT UL (ms)': [100, 200, 300, None],
    'Event': ['Event 1', 'Event 2', 'Event 3', 'Event 4']
}

# Create DataFrame
df = pd.DataFrame(data)

# Ensure 'Start' column is in datetime format and handle invalid dates
df['Start'] = pd.to_datetime(df['Start'], errors='coerce')  # Invalid dates will be turned into NaT

# Ensure 'Avg RTT UL (ms)' column is numeric and handle invalid data
df['Avg RTT UL (ms)'] = pd.to_numeric(df['Avg RTT UL (ms)'], errors='coerce')  # Invalid numbers will be turned into NaN

# Drop rows with NaT in 'Start' or NaN in 'Avg RTT UL (ms)' columns
df = df.dropna(subset=['Start', 'Avg RTT UL (ms)'])

# Check if 'Avg RTT UL (ms)' exists in the DataFrame
if 'Avg RTT UL (ms)' in df.columns:
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting the line chart
    ax.plot(df['Start'], df['Avg RTT UL (ms)'], label='Avg RTT UL (ms)', color='blue')

    # Set plot title and labels
    ax.set_title('Average RTT UL (ms) Over Time')
    ax.set_xlabel('Start Time')
    ax.set_ylabel('Avg RTT UL (ms)')

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45)

    # Display legend
    ax.legend()

    # Show the plot in Streamlit
    st.pyplot(fig)
else:
    st.error("Column 'Avg RTT UL (ms)' not found in the dataset.")


    fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df['Avg RTT UL (ms)'], bins=5, color='orange', edgecolor='black', label='Avg RTT UL (ms)')
ax.set_title('Histogram of Avg RTT UL (ms)')
ax.set_xlabel('Avg RTT UL (ms)')
ax.set_ylabel('Frequency')
ax.legend()
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df['Start'], df['Avg RTT UL (ms)'], color='purple', label='Avg RTT UL (ms)')
ax.set_title('Bar Chart of Avg RTT UL (ms) Over Time')
ax.set_xlabel('Start Time')
ax.set_ylabel('Avg RTT UL (ms)')
plt.xticks(rotation=45)
ax.legend()
st.pyplot(fig)


