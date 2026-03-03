# Use an official Python slim image
FROM python:3.11-slim

# Install system dependencies and the Microsoft ODBC Driver 18
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    apt-utils \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get install -y unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your scripts (db_test.py, .env, etc.)
COPY . .

# Run the test script by default
CMD ["python", "db_test.py"]