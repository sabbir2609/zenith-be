# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the .env file and set environment variables
COPY .env /app/
ENV $(cat .env | grep -v ^# | xargs)

# Copy the current directory contents into the container at /app
COPY . /app/

# Collect static files (if needed)
RUN python manage.py collectstatic --noinput

# Expose the port that Uvicorn will run on
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-level", "debug", "--reload"]
