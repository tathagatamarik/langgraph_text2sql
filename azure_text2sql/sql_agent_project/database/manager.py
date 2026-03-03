# Database execution logic goes here
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

class AzureSQLManager:
    def __init__(self):
        self.conn_str = (
            f"Driver={{ODBC Driver 18 for SQL Server}};"
            f"Server=tcp:{os.getenv('DB_SERVER')},1433;"
            f"Database={os.getenv('DB_NAME')};"
            f"Uid={os.getenv('DB_USER')};"
            f"Pwd={os.getenv('DB_PWD')};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
        )

    def run_query(self, sql_query):
        """
        Executes the provided SQL and returns the result set.
        """
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                
                # Check if the query returns rows (SELECT) or not (INSERT/UPDATE)
                if cursor.description:
                    columns = [column[0] for column in cursor.description]
                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    return {"status": "success", "data": results}
                else:
                    conn.commit()
                    return {"status": "success", "message": "Query executed successfully."}
                    
        except Exception as e:
            return {"status": "error", "message": str(e)}