import os
import pyodbc
import random
from dotenv import load_dotenv

load_dotenv()

conn_str = (
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server=tcp:{os.getenv('DB_SERVER')},1433;"
    f"Database={os.getenv('DB_NAME')};"
    f"Uid={os.getenv('DB_USER')};"
    f"Pwd={os.getenv('DB_PWD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def bulk_insert_data(num_rows=100):
    # Prepare synthetic data
    categories = ['Electronics', 'Furniture', 'Stationery', 'Software']
    data_to_insert = []
    
    for i in range(200, 200 + num_rows):
        data_to_insert.append((
            i, 
            f"Product_{i}", 
            random.choice(categories), 
            random.randint(1, 1000), 
            round(random.uniform(10.0, 500.0), 2)
        ))

    try:
        with pyodbc.connect(conn_str) as conn:
            # IMPORTANT: This makes bulk inserts 10x faster
            conn.autocommit = False 
            cursor = conn.cursor()
            cursor.fast_executemany = True 
            
            sql = "INSERT INTO Inventory (ItemID, ItemName, Category, StockCount, PricePerUnit) VALUES (?, ?, ?, ?, ?)"
            
            print(f"Starting bulk insert of {num_rows} rows...")
            cursor.executemany(sql, data_to_insert)
            conn.commit()
            print("✅ Bulk insertion completed successfully.")
            
    except Exception as e:
        print(f"❌ Bulk insert failed: {e}")

if __name__ == "__main__":
    bulk_insert_data(100)