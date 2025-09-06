FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies directly
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir requests python-dotenv

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash eribot
RUN chown -R eribot:eribot /app
USER eribot

# Command to run the application
CMD ["python", "simple_bot.py"]
