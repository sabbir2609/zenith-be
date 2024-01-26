FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /home/app

# Install required system packages
RUN apt-get update && apt-get install -y python3-dev libpq-dev

# Install pipenv
RUN pip install --upgrade pip

# Install application dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy wait-for-it.sh and set execute permission
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x ./wait-for-it.sh

# Copy docker-entrypoint.sh and set execute permission
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

# Copy application files
COPY . .

# Expose port 8000 on the container
EXPOSE 8000
