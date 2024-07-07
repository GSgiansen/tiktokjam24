# Use a larger base image to accommodate space requirements
FROM python:3.9

# Set the working directory
WORKDIR /backend

# Install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container at /backend
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the content of the local backend directory to /backend in the container
COPY . .

# Copy the .env file to /backend/.env
COPY .env .

# # Entrypoint script to wait for Airflow services and then start the FastAPI application
# COPY wait-for-airflow.sh /backend/wait-for-airflow.sh

# # Set executable permissions for the script
# RUN chmod +x /backend/wait-for-airflow.sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI application
# CMD ["/backend/wait-for-airflow.sh", "airflow-webserver", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["fastapi", "run", "main.py", "--port", "8000"]
