import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch credentials
db_params = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

# Connect and test
try:
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM mag7;")
    row_count = cur.fetchone()[0]
    print(f"✅ Connection successful. mag7 table contains {row_count} rows.")

    cur.close()
    conn.close()

except Exception as e:
    print(f"❌ Connection failed: {e}")
