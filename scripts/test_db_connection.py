import psycopg2

# Replace <your_password> with your actual PostgreSQL password
conn = psycopg2.connect(
    host="localhost",           # PostgreSQL host (localhost if on your local machine)
    database="xdr_data_db
    
    
    ",         # Name of the database you're connecting to
    user="postgres",            # PostgreSQL username (default is "postgres")
    password="8128"  # Your PostgreSQL password
)

print("Connection successful!")
