# Distributed Code Execution Platform

A platform for safely running user code in multiple programming languages inside isolated Docker containers. This is a backend-oriented project built with FastAPI + Celery + Docker SDK, with a simple vanilla JS frontend for demonstration.

## Deployment

The service is deployed on a VPS and is available at https://coderun.pp.ua/. Swagger documentation is available at https://coderun.pp.ua/docs.

Test credentials:

`test@gmail.com`

`testpassword`

## Features

- Code execution in isolated Docker containers with no network access and CPU/memory limits
- Support for 6 languages: Python, JavaScript, C++, Go, Java, Rust
- Asynchronous job processing through a queue (Celery + RabbitMQ)
- JWT authentication with access and refresh tokens
- Automatic cleanup of old records on a schedule (Celery Beat)
- A web interface with syntax highlighting and autocomplete (CodeMirror)

## Architecture

```
Browser → nginx → api-service (FastAPI) → RabbitMQ → worker (Celery) → Docker containers
                          ↓                                    ↓
                      PostgreSQL ←───────────────────────────────
```

- nginx serves frontend static files and proxies /auth/* and /jobs/* to the backend
- api-service receives requests, creates jobs in the database, and publishes tasks to the queue
- worker pulls tasks from the queue, starts a Docker container, executes code, and stores the result
- beat schedules cleanup tasks for old records
- api-service and worker do not communicate directly over HTTP; they communicate through the task queue (RabbitMQ), which allows workers to scale independently from the API

## Stack

### Backend
- Python
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Alembic
- pytest

### Messaging
- Celery
- RabbitMQ

### Containerization
- Docker SDK for Python
- Docker Compose

### Authentication
- JWT

### Frontend
- Vanilla JavaScript
- CodeMirror 5
- nginx

## Supported Languages

| Language | Docker image | Execution method |
|---|---|---|
| Python | python:3.12-slim | interpreted |
| JavaScript | node:20-alpine | interpreted |
| C++ | gcc:13 | compile + run |
| Go | golang:1.22-alpine | compile + run |
| Java | eclipse-temurin:21-jdk | compile + run |
| Rust | rust:1.77-slim | compile + run |

## Isolation and Security

- Each job runs in a separate disposable container (`--rm`)
- Network access inside the container is disabled (`network_disabled`)
- Memory and CPU limits are enforced (`mem_limit`, `cpu_quota`)
- Execution is time-limited and the container is forcefully stopped if the limit is exceeded
- Code is passed into the container as a base64-encoded string through the startup command, without mounting files from the host

## Running the Project

1. Clone the repository and create a `.env` file with the Postgres, RabbitMQ, and JWT secret variables

```
git clone https://github.com/Polkovniku/Distributed-Code-Execution-Platform.git
```

```
POSTGRES_DB=distributed_code_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
RABBITMQ_DEFAULT_USER=your_user
RABBITMQ_DEFAULT_PASS=your_password
SECRET_KEY=your_secret_key
DB_HOST=db
RABBITMQ_HOST=rabbitmq
```

2. Start the services

```
docker compose up --build
```

3. Open the main page

```
http://localhost:8081/
```

## API

Full Swagger documentation is available at http://localhost:8081/docs after startup.

### Main Endpoints

- POST /auth/register - register a user
- POST /auth/login - sign in and return access/refresh tokens
- POST /auth/token - refresh the access token using a refresh token
- GET /auth/me - get the current user
- POST /jobs/ - create a job (code + language)
- GET /jobs/{id} - get the execution status and result
- GET /jobs/ - list the user's jobs

### Stopping the Services

```
docker compose down
```

## Tests

The backend is covered by pytest tests with a separate test database (`test-db` service in docker-compose).

### Running Tests

You need `uv` installed and synchronized dependencies:

```
cd app-service
uv sync
docker compose --profile test up -d test-db
uv run pytest
```

### Stopping the Test Database

```
docker compose --profile test down
```

## Example

<img width="1854" height="907" alt="Снимок экрана 2026-08-18 154504" src="https://github.com/user-attachments/assets/9d6acb18-e6ed-489c-ba72-3b4a3539d944" />
