FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir slack_sdk requests

WORKDIR /app

COPY . .

CMD ["python", "-m", "freshworks_tools"]