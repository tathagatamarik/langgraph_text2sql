import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

# Reuse connection string from above
conn_str = (
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server=tcp:{os.getenv('DB_SERVER')},1433;"
    f"Database={os.getenv('DB_NAME')};"
    f"Uid={os.getenv('DB_USER')};"
    f"Pwd={os.getenv('DB_PWD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

def run_test_queries():
    queries = {
        "Total Stock by Category": "SELECT Category, SUM(StockCount) FROM Inventory GROUP BY Category",
        "Top 5 Most Expensive Items": "SELECT TOP 5 ItemName, PricePerUnit FROM Inventory ORDER BY PricePerUnit DESC",
        "Out of Stock Check": "SELECT ItemName FROM Inventory WHERE StockCount = 0"
    }

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            for description, sql in queries.items():
                print(f"\n--- {description} ---")
                cursor.execute(sql)
                rows = cursor.fetchall()
                if not rows:
                    print("No data found.")
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"❌ Query test failed: {e}")

if __name__ == "__main__":
    run_test_queries()