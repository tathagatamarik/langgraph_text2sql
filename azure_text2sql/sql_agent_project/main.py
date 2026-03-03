# Entry point for orchestration
from agents.generator import QueryGenerator
from agents.validator import QueryValidator
from database.manager import AzureSQLManager
import logging

def main():
    query_gen = QueryGenerator()
    query_val = QueryValidator()
    db_manager = AzureSQLManager()
    
    user_input = input("Enter your data question: ")
    
    max_retries = 3
    feedback = None
    final_sql = None

    for attempt in range(max_retries):
        print(f"\n[Attempt {attempt+1}] Generating SQL...")
        sql = query_gen.generate(user_input, feedback)
        
        print(f"Reviewing SQL: {sql}")
        validation_result = query_val.validate(sql)
        
        if validation_result == "VALID":
            print("✅ SQL Validated. Executing...")
            final_sql = sql
            break
        else:
            print(f"❌ Validation Failed: {validation_result}")
            feedback = validation_result

    if final_sql:
        result = db_manager.run_query(final_sql)
        if result['status'] == 'success':
            print("\n--- Results ---")
            print(result['data'])
        else:
            print(f"Runtime Error: {result['message']}")
    else:
        print("Failed to generate a valid query after multiple retries.")

if __name__ == "__main__":
    main()