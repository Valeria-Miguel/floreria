
#FROM mcr.microsoft.com/devcontainers/python:3.9

# [Optional] If your requirements.txt is in the root of your project, uncomment the following lines
#COPY ../requirements.txt /tmp/pip-tmp/
#RUN pip install --no-cache-dir -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# Use an official Python runtime as the base image.
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logging.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container.
WORKDIR /app

# Install system dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies.
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code.
COPY . /app/

# Expose port 8000 for the Django application.
EXPOSE 8000

# Define the command to run the application using Gunicorn.
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
