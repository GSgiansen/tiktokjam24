# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /backend

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy the requirements.txt file into the container at /backend
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the content of the local backend directory to /backend in the container
COPY . .

# Copy .env file if needed
COPY .env /backend.env

# Expose the port the app runs on
EXPOSE 8000

# Copy the wait-for-service script and set permissions
COPY wait-for-service.sh /wait-for-service.sh
RUN chmod +x /wait-for-service.sh

# Command to run the FastAPI application, using the wait-for-service script
CMD ["/wait-for-service.sh", "airflow-webserver", "fastapi", "run", "main.py", "--port", "8000"]
