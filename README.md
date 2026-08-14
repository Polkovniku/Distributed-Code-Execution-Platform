# Distributed Code Execution Platform

Платформа для безпечного запуску персонального коду на різних мовах програмування в ізольованих Docker-контейнерах. Backend-орієнтований проект: FastAPI + Celery + Docker SDK, із простим vanilla JS фронтендом для демонстрації.

## Деплой
Сервіс розмещенний на VPS та доступний за посиланням https://coderun.pp.ua/ , також  документація Swagger за https://coderun.pp.ua/docs

## Можливости

- Запуск коду в ізольованих Docker-контейнерах (без мережі, з лімітами CPU/пам'яті)
- Підтримка 6 мов: Python, JavaScript, C++, Go, Java, Rust
- Асинхронна обробка завдань через чергу (Celery + RabbitMQ)
- JWT-аутентифікація (access + refresh токени)
- Автоматичне очищення старих записів за розкладом (Celery Beat)
- Веб-інтерфейс з підсвічуванням синтаксису та автодоповненням (CodeMirror)

## Архітектура

```
Browser → nginx → api-service (FastAPI) → RabbitMQ → worker (Celery) → Docker containers
                          ↓                                    ↓
                      PostgreSQL ←───────────────────────────────
```


- nginx - роздає статику фронтенду, проксує /auth/* та /jobs/* на бекенд
- api-service - приймає запити, створює job у БД, публікує завдання в чергу
- worker - забирає завдання з черги, піднімає Docker-контейнер, виконує код, зберігає результат
- beat — за розкладом надсилає завдання очищення старих записів
- Api-service та worker спілкуються не напряму (HTTP), а через чергу завдань (RabbitMQ) – це дозволяє масштабувати воркери незалежно від API

## Стек

### Backend: 
- Python 
- FastAPI 
- SQLAlchemy (async)
- PostgreSQL
- Alembic 
- pytest

### Messaging: 
- Celery 
- RabbitMQ 

### Containerization
- Docker SDK for Python
- Docker Compose

### Authentication
- JWT 

### Frontend: 
- Vanilla JavaScript, 
- CodeMirror 5, 
- nginx

## Поддерживаемые языки

| Язык | Docker-образ | Спосіб виконання |
|---|---|---|
| Python | python:3.12-slim | інтерпретація |
| JavaScript | node:20-alpine | інтерпретація |
| C++ | gcc:13 | компіляція + запуск |
| Go | golang:1.22-alpine | компіляція + запуск |
| Java | eclipse-temurin:21-jdk | компіляція + запуск |
| Rust | rust:1.77-slim | компіляція + запуск |

## Ізоляція та безпека
- Кожен job виконується в окремому одноразовому контейнері (-rm)
- Мережа всередині контейнера вимкнена (network_disabled)
- Обмеження по пам'яті та CPU (mem_limit, cpu_quota)
- Таймаут на виконання – контейнер примусово вбивається при перевищенні
- Код передається в контейнер як base64-encoded рядок через команду запуску (без монтування файлів з хоста)

## Запуск проекту

1. Скопіювати репозиторій та створити .env файл (змінні для Postgres, RabbitMQ, JWT-секретів)

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

2. Підняти сервіси

```
docker compose up --build
```

3. Головна сторінка

```
http://localhost:8081/
```


## API

Повна документація Swagger доступна на http://localhost:8081/docs після запуску.

### Основные эндпоинты
- POST /auth/register - реєстрація
- POST /auth/login - вхід, повертає access/refresh токени
- POST /auth/token - оновлення access-токена по refresh-токену
- GET /auth/me - отримання користувача
- POST /jobs/ - створити job (код + мова)
- GET /jobs/{id} — отримати статус та результат виконання
- GET /jobs/ — список job'ів користувача

### Зупинення сервісів

```
docker compose down
```

## Тести

Backend покритий тестами на pytest з окремою тестовою БД (test-db сервіс у docker-compose).

### Запуск тестів
Потрібен встановлений `uv` та синхронізовані залежності:

```
cd app-service
uv sync
docker compose --profile test up -d test-db
uv run pytest
```

### Зупинка тестової БД

```
docker compose --profile test down
```


## Приклад роботи

<img width="1411" height="883" alt="Снимок экрана 2026-08-14 135156" src="https://github.com/user-attachments/assets/d6216fd3-1169-4cf6-9017-fbbad1796ab4" />
