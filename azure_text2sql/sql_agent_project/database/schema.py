# Schema retrieval logic goes here
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_schema():
    """
    Connects to Azure SQL and retrieves metadata for all user-defined tables.
    Returns a formatted string for the LLM context.
    """
    conn_str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server=tcp:{os.getenv('DB_SERVER')},1433;"
        f"Database={os.getenv('DB_NAME')};"
        f"Uid={os.getenv('DB_USER')};"
        f"Pwd={os.getenv('DB_PWD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )

    schema_context = "DATABASE SCHEMA:\n"
    
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            # Query to get Table Name, Column Name, and Data Type
            query = """
                SELECT t.name AS TableName, c.name AS ColumnName, ty.name AS DataType
                FROM sys.tables t
                JOIN sys.columns c ON t.object_id = c.object_id
                JOIN sys.types ty ON c.user_type_id = ty.user_type_id
                WHERE t.is_ms_shipped = 0
                ORDER BY t.name, c.column_id
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            current_table = ""
            for row in rows:
                if row.TableName != current_table:
                    current_table = row.TableName
                    schema_context += f"\nTable: {current_table}\nColumns:\n"
                schema_context += f"  - {row.ColumnName} ({row.DataType})\n"
                
        return schema_context
    except Exception as e:
        return f"Error retrieving schema: {str(e)}"

if __name__ == "__main__":
    # Test the schema retrieval locally
    print(get_db_schema())