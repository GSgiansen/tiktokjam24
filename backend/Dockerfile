# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /backend

# Copy the requirements.txt file into the container at /backend
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the content of the local backend directory to /backend in the container
COPY . .

COPY .env /backend.env

# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["fastapi", "dev", "main.py"]
