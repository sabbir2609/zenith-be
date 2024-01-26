FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y python3-dev libpq-dev \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --upgrade pip

# Install application dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy wait-for-it.sh and set execute permission
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Copy docker-entrypoint.sh and set execute permission
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Copy application files
COPY . ./app/


# Expose port 8000 on the container
EXPOSE 8000
