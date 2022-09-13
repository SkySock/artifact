# Artifact API

Backend API платформы для продвижения и монетизации творческого контента.

**Стек:**
- Python >= 3.10
- Django Rest Framework
- PostgreSQL
- Celery

### Запуск с Docker

1. Склонировать репозиторий
2. В корне проекта создать и заполнить файл `.env.dev`
```
DEBUG=1
SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS='localhost 127.0.0.1'

CORS_ALLOWED_ORIGINS='http://your-domain'

DATABASE=postgres
POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_DB=artifact
POSTGRES_USER=artifact_user
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_PASSWORD=artifact_password

TELEGRAM_BOT_TOKEN=your_telegram_bot_token

RABBIT_HOST='broker'
RABBIT_PORT=5672
```
3. Собрать образ
```
docker-compose build
```
4. Запустить
```
docker-compose up
```
5. Создать и применить миграции
```commandline
docker exec -ti artifact-api-1 /bin/bash
```
```commandline
poetry run ./src/manage.py makemigrations
poetry run ./src/manage.py migrate
```
6. Запуск тестов
```commandline
docker exec artifact-api-1 poetry run ./src/manage.py test
```

### Swager UI
http://127.0.0.1:25566/api/v1/schema/swagger-ui/
