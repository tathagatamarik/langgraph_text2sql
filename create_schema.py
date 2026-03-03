import os
import pyodbc
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

def initialize_table():
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            print("Creating Inventory table...")
            
            # T-SQL Syntax for Azure SQL
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Inventory]') AND type in (N'U'))
                BEGIN
                    CREATE TABLE [dbo].[Inventory] (
                        [ItemID] INT PRIMARY KEY,
                        [ItemName] NVARCHAR(100) NOT NULL,
                        [Category] NVARCHAR(50),
                        [StockCount] INT DEFAULT 0,
                        [PricePerUnit] DECIMAL(10, 2)
                    )
                END
            """)
            conn.commit()
            print("✅ Table [dbo].[Inventory] is ready.")
            
    except Exception as e:
        print(f"❌ Table creation failed: {e}")

if __name__ == "__main__":
    initialize_table()