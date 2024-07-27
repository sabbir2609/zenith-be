# General Instructions:
- If you are using PostgreSQL and Redis inside Docker, ensure to update the .env configuration accordingly.
- Upgrade to Django 5.
- Be aware that django-celery-beat version 2.5.0 is incompatible with Django version 5.0.1. It requires a Django version less than 5.0.



# Docker commands

This section contains a series of Docker commands used for building and running a Docker container.

- `COPY ./requirements.txt /requirements.txt`: Copies the `requirements.txt` file from the local directory to the `/requirements.txt` path inside the Docker container.
- `RUN apk add --update --no-cache postgresql-client jpeg-dev`: Installs the `postgresql-client` and `jpeg-dev` packages using the Alpine package manager (`apk`).
- `RUN apk add --update --no-cache --virtual .tmp-build-deps \ 
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev`: Installs additional development dependencies using `apk`. These dependencies are later removed to reduce the size of the final Docker image.
- `RUN pip install -r /requirements.txt`: Installs Python packages listed in the `requirements.txt` file using `pip`.
- `RUN apk del .tmp-build-deps`: Removes the temporary build dependencies installed earlier.
- `docker-compose up -d --build`: Builds and starts the Docker containers defined in the `docker-compose.yml` file in detached mode (`-d`).

Please note that this documentation comment is specific to the Markdown file located at `/home/sabbir/zenith-sys/zenith/resource/Instruction.md`.

# Management Commands

This section contains various management commands for different purposes.

## PostgreSQL Commands

- `sudo service postgresql start`: Starts the PostgreSQL service.
- `sudo service postgresql stop`: Stops the PostgreSQL service.
- `sudo -u postgres psql`: Opens the PostgreSQL command-line interface as the `postgres` user.
- `CREATE DATABASE zenith;`: Creates a new database named `zenith`.
- `\q`: Exits the PostgreSQL command-line interface.
- `sudo -u postgres psql zenith`: Opens the PostgreSQL command-line interface for the `zenith` database.
- `ALTER USER postgres with encrypted password 'your_password';`: Changes the password for the `postgres` user.

## Redis Command
- `redis-server`: start the the Redis server
- `redis-cli shutdown`: Shutsdown the Redis server.

## Mosquitto Commands

- `sudo pkill mosquitto`: Stops the Mosquitto MQTT broker.
- `ps -ef | grep mosquitto`: Lists the processes containing the word "mosquitto".
- `sudo kill 'pid of mosquitto'`: Kills the process with the specified PID.

## Server Command

- `uvicorn core.asgi:application --port 8000 --workers 4 --log-level debug --reload`: Starts the Uvicorn ASGI server with specified configurations.

- `gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker`: Starts the Gunicorn with Uvicorn ASGI server with specified configurations.

- `hypercorn --bind '0.0.0.0:8000' core.asgi:application`: Starts the Hypercorn ASGI server with specified configurations.

## Celery Commands

- `celery -A core worker --loglevel=info`: Starts a Celery worker.
- `celery -A core beat`: Starts the Celery beat scheduler.
- `celery -A core flower`: Starts the Celery Flower monitoring tool.



# Room List Endpoint Documentation

## Endpoint: `api/main/rooms/`

This endpoint is used to retrieve a list of rooms. It supports a variety of filters that allow you to narrow down the list of rooms based on specific criteria. 

## Filters

You can apply filters by appending them to the URL as query parameters. Here's an example of a URL with filters:

`/api/main/room/?floor=&room_type=4&room_type__price=&room_type__price__lt=&room_type__price__gt=&is_available=&capacity=&capacity__lt=&capacity__gt=`

Here's a breakdown of each filter:

- `floor`: Filter rooms based on the floor they are located on.
- `room_type`: Filter rooms based on their type.
- `room_type__price`: Filter rooms with a price exactly equal to a certain value.
- `room_type__price__lt`: Filter rooms with a price less than a certain value.
- `room_type__price__gt`: Filter rooms with a price greater than a certain value.
- `is_available`: Filter rooms based on their availability.
- `capacity`: Filter rooms with a capacity exactly equal to a certain value.
- `capacity__lt`: Filter rooms with a capacity less than a certain value.
- `capacity__gt`: Filter rooms with a capacity greater than a certain value.

## Search

In addition to these filters, the endpoint also supports a search functionality. You can search for rooms by appending a `search` query parameter to the URL. Here's an example:

`/api/main/room/?search=business`

This would return rooms that match the search term "business".

## Additional Functionality 

To verify room availability, execute a GET request to `api/room/available/?start_date=2022-01-01&end_date=2022-01-31`. This will return a list of all rooms available within the specified date range.


# Used Services

This section provides details about the services used in the project.

## PostgreSQL
We are using the PostgreSQL service provided by `neon.tech`. PostgreSQL is a powerful, open-source object-relational database system that uses and extends the SQL language combined with many features that safely store and scale the most complicated data workloads.

## Redis
Our Redis service is hosted on `app.redislabs.com/`. Redis is an open-source, in-memory data structure store, used as a database, cache, and message broker. It supports various data structures such as Strings, Hashes, Lists, Sets, etc.

## File Storage
For file storage, we are using `cloudinary`. Cloudinary is a cloud-based service that provides an end-to-end image and video management solution including uploads, storage, manipulations, optimizations and delivery.
