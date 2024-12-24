import psycopg2

def export_to_postgres(data):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="xdr_data_db",  # Replace with your database name
            user="postgres",         # Replace with your username
            password="8128"          # Replace with your password
        )
        cursor = conn.cursor()

        # Create table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_scores (
            user_id INT PRIMARY KEY,
            engagement_score FLOAT,
            experience_score FLOAT,
            satisfaction_score FLOAT
        )
        """)

        # Insert data
        for _, row in data.iterrows():
            cursor.execute("""
            INSERT INTO user_scores (user_id, engagement_score, experience_score, satisfaction_score)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE
            SET 
                engagement_score = EXCLUDED.engagement_score,
                experience_score = EXCLUDED.experience_score,
                satisfaction_score = EXCLUDED.satisfaction_score
            """, (row["user_id"], row["engagement_score"], row["experience_score"], row["satisfaction_score"]))

        conn.commit()
        print("Data successfully exported to PostgreSQL!")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()
