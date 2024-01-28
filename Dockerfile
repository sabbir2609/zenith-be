# Use the official Python image with version 3.10
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Ensure execute permissions for scripts
RUN chmod +x /app/wait-for-it.sh /app/docker-entrypoint.sh

# Expose the port on which your Django app will run
EXPOSE 8000

# Run wait-for-it.sh to check if the PostgreSQL port is open, then run docker-entrypoint.sh
CMD ["./wait-for-it.sh", "postgres:5432", "--", "./docker-entrypoint.sh"]
