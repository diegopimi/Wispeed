# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt-get update

RUN apt-get update && \
    apt-get install -y default-jre default-jdk graphviz && \
    # Remove temporary files
    rm -rf /var/lib/apt/lists/*


# Expose ports
EXPOSE 5000

CMD ["python", "app.py"]