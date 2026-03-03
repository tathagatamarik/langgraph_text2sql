import os

def create_project_structure():
    # Define the directory structure
    project_root = "sql_agent_project"
    folders = [
        "database",
        "agents",
        "utils",
    ]

    # Define the files and their initial content
    files = {
        ".env": "DB_SERVER=your-server.database.windows.net\nDB_NAME=your-db\nDB_USER=your-user\nDB_PWD=your-password\nOPENAI_API_KEY=your-key",
        "requirements.txt": "pyodbc\npython-dotenv\nlangchain\nlangchain-openai\nlanggraph\npyyaml",
        "prompt.yaml": "query_generator:\n  system_message: 'Your generator prompt here'\nquery_validator:\n  system_message: 'Your validator prompt here'",
        "database/__init__.py": "",
        "database/manager.py": "# Database execution logic goes here",
        "database/schema.py": "# Schema retrieval logic goes here",
        "agents/__init__.py": "",
        "agents/generator.py": "# Generator agent logic",
        "agents/validator.py": "# Validator agent logic",
        "utils/__init__.py": "",
        "utils/logger.py": "import logging\nlogging.basicConfig(level=logging.INFO)",
        "main.py": "# Entry point for orchestration"
    }

    # Create folders
    if not os.path.exists(project_root):
        os.makedirs(project_root)
        print(f"Created project root: {project_root}")

    for folder in folders:
        path = os.path.join(project_root, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created folder: {path}")

    # Create files
    for file_path, content in files.items():
        full_path = os.path.join(project_root, file_path)
        with open(full_path, "w") as f:
            f.write(content)
            print(f"Created file: {full_path}")

    print("\n✅ Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()