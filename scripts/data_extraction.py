import pandas as pd
import psycopg2

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
