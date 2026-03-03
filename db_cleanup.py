import pyodbc
from db_setup import conn_str # Import your verified connection string

def close_connection_gracefully():
    conn = None
    try:
        print("Connecting to Azure SQL for a session...")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Perform a dummy operation
        cursor.execute("SELECT 1")
        print("Session active.")

    except Exception as e:
        print(f" Error during session: {e}")
        
    finally:
        # This block runs NO MATTER WHAT (even if the code above fails)
        if conn:
            conn.close()
            print(" Connection closed successfully. Resources released.")

if __name__ == "__main__":
    close_connection_gracefully()