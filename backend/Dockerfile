# Use Python as the base image
FROM python:3-slim

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container's /app directory
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the main script
CMD ["python", "main.py"]
