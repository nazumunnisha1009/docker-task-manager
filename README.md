
# DevSprint'26 - Dockerized Task Manager

## Project Overview
A simple task management web application built with Python and Flask and packaged using Docker.

Users can add tasks and mark them as complete.

## Technologies Used
- Python 3.12
- Flask
- Docker
- Docker Compose

## Requirements
Docker Desktop must be installed and running.

Python and Flask do not need to be installed on the host machine.

## Project Files
- app.py - Application source code
- requirements.txt - Python dependencies
- Dockerfile - Docker image instructions
- compose.yaml - Container configuration
- .env - Application environment variables
- .dockerignore - Files excluded from the build context

## Build and Run
Open the terminal in the project directory and execute:

    docker compose up --build -d

Open this URL in your browser:

    http://localhost:5000

## Check Container Status

    docker compose ps
## Verify Dependencies Inside the Container

Check the Python version:

```bash
docker compose exec app python --version
```

Check the installed Flask dependency:

```bash
docker compose exec app pip show Flask
```

These commands verify that Python and Flask are available inside the running container.

## Rebuild the Application

```bash
docker compose down
docker compose up --build -d
```

The Docker image contains the application runtime and required dependencies, so Python and Flask do not need to be installed manually on the host machine.

## Expected Result

- Docker image builds successfully.
- The application container starts and runs.
- The task manager opens at `http://localhost:5000`.
- Users can add tasks and mark them as complete.

## View Application Logs

    docker compose logs app

## Stop the Application

    docker compose down

## Environment Variables
APP_NAME sets the application title.
PORT sets the application port.

## Limitation
Tasks are stored in memory and reset when the application restarts.
## Environment Variable Verification

The application uses environment variables to configure its title and port.

- `APP_NAME` sets the application title.
- `PORT` sets the application port.

### Test APP_NAME Configuration

1. Open the `.env` file.
2. Change `APP_NAME` to a new value, for example:

   ```env
   APP_NAME=DevSprint Demo
   PORT=5000
   ```

3. Save the `.env` file.
4. Restart the application with Docker Compose:

   ```bash
   docker compose up --build -d
   ```

5. Open `http://localhost:5000` in a browser and verify that the application title has changed.

6. Verify the environment variable inside the running container:

   ```bash
   docker compose exec app printenv APP_NAME
   ```

The command should display the updated application name.

This confirms that Docker Compose passes the environment variable to the container and that the application uses it for configuration.
