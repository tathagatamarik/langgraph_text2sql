import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

# Build connection string - Note the Linux driver path/name
conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};" # Same name, but maps to Linux driver inside Docker
    f"Server=tcp:{os.getenv('DB_SERVER')},1433;"
    f"Database={os.getenv('DB_NAME')};"
    f"Uid={os.getenv('DB_USER')};"
    f"Pwd={os.getenv('DB_PWD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def check_db():
    try:
        with pyodbc.connect(conn_str) as conn:
            print("  successfully connected to Azure SQL!")
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            print(f"Database Version: {cursor.fetchone()[0]}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    check_db()