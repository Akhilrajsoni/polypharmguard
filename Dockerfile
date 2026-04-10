FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Upgrade pip + install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Download spacy model
RUN python -m spacy download en_core_web_sm

# Expose port
EXPOSE 8080

# Start app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
