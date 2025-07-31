# Use python 3.10 slim
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the dependencies file first (better cache)
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port that will be used by Cloud Run
EXPOSE 8080

# Environment variable 
ENV PORT=8080

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]