# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update package lists before installing
RUN apt-get update

# Update package lists before installing
RUN apt-get update && \
    # Install system dependencies
    apt-get install -y default-jre default-jdk graphviz && \
    # Install Python dependencies
    pip install Flask Flask-PyMongo pymongo plantuml && \
    # Remove temporary files
    rm -rf /var/lib/apt/lists/*

# Create directory for MongoDB data
RUN mkdir -p /data/db

# Expose ports
# EXPOSE 27017
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]