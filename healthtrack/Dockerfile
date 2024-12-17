FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create uploads directory
RUN mkdir -p uploads/medical_records

# Set Python path
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Create Streamlit config directory and config file
RUN mkdir -p /root/.streamlit
COPY config.toml /root/.streamlit/config.toml

# Expose the port Streamlit runs on
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]