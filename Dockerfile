# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install Flask Flask-PyMongo pymongo

# Install PlantUML
RUN apt-get update && apt-get install -y \
    default-jre \
    default-jdk \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

RUN pip install plantuml

# Expose port 5000 to the outside world
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]