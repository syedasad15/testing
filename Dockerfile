# FROM python:3.12-slim

# # Set working directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy all app files
# COPY . .

# # Streamlit will run on port 8080 for Cloud Run
# EXPOSE 8080

# # Run Streamlit app
# CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]


# FROM python:3.12-slim

# # Set working directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy all app files   best
# COPY . .

# # Expose port (Cloud Run expects this, but real binding comes from $PORT)
# EXPOSE 8080

# # Run Streamlit app (use Cloud Run's PORT env variable)
# CMD ["sh", "-c", "streamlit run main.py --server.port=$PORT --server.address=0.0.0.0"]

# FROM python:3.12-slim

# # Set working directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# best hhh
# # Copy all app files   
# COPY . .

# # Expose port (Cloud Run expects this, but real binding comes from $PORT)
# EXPOSE 8080

# # Run FastAPI app (use Cloud Run's PORT env variable)
# CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port $PORT"] 


FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (including Poppler)
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose port (Cloud Run expects this, but real binding comes from $PORT)
EXPOSE 8080

# Run FastAPI app (use Cloud Run's PORT env variable)
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port $PORT"]

# # Use Python base image
# FROM python:3.10-slim

# # Set working directory
# WORKDIR /app

# # Install system dependencies if needed
# COPY packages.txt .
# RUN apt-get update && xargs -a packages.txt apt-get install -y

# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install fastapi uvicorn

# # Copy project files
# COPY . .

# # Expose ports (Streamlit default 8501, API 8000)
# EXPOSE 8501
# EXPOSE 8000

# # Environment variable to select mode
# ENV APP_MODE=api

# # Default command: run API
# CMD if [ "$APP_MODE" = "streamlit" ]; then \
#         streamlit run main.py --server.port=8501 --server.address=0.0.0.0; \
#     else \
#         uvicorn api:app --host 0.0.0.0 --port 8000 --reload; \
#     fi

