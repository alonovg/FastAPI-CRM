# CRM Система для учёта заказов

Данный проект выполнен как "PET-Project", для оттачивания следующих навыков:
- Создание собственного API
- Создание приложения, построенного на микро-сервисной архитектуре
- Использование принципа MVC
- Работа с асинхронными запросами
- Разработка архитектуры БД
- Выполнение ``["POST", "GET", "DELETE", "PUTCH"]`` запросов к БД на PostgreSQL
- Валидация данных с помощью pydantic
- Создание простой Админ панели с помощью SQLAdmin
- Кэширование с помощью Redis
- Фоновые задачи с Celery
- Просмотр очередей через Flower
- Тестирование с помощью PyTest (Unit/Integration)
- Логирование с помощью Sentry
- Сбор метрик с Prometheus
- Мониторинг с Grafana

## Usage:
- Alembic generate version:
``alembic revision --autogenerate -m "Initial migration``
- Alembic make migrations:
``alembic upgrade head``
- Main app: ``uvicorn app.main:app``
- Celery: ``celery -A app.tasks.celery_task:celery worker --loglevel=INFO --pool=solo``
- Flower: ``celery -A app.tasks.celery_task:celery flower``

## Docker build:
``docker compose build``
``docker compose up``

## Links:
- Host: ``/localhost:9000``
- Swagger: ``/docs``
- ReDoc: ``/redoc``
- Flower: ``/localhost:5555``
- Prometheus: ``/localhost:9090``
- Grafana: ``/localhost:3000``


## Environment Variables

To run this project, you will need to add the following environment variables to .env file

Для подключения к БД:
- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASS`
- `DB_NAME`

Для SMTP отправки:
- `FRONTEND_URL`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASS`

Для Redis:
- `REDIS_HOST`
- `REDIS_PORT`

Для JWT & password:
- `SECRET_KEY`
- `ALGORITHM`