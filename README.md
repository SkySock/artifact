# Artifact API

Backend API платформы для продвижения и монетизации творческого контента.

**Стек:**
- Python >= 3.10
- Django Rest Framework
- PostgreSQL
- Celery

### Запуск с Docker

1. Склонировать репозиторий
2. В корне проекта создать и заполнить файл .end.dev
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

REDIS_HOST='redis'
REDIS_PORT=6379
```
3. Собрать образ
```
docker-compose build
```
4. Запустить
```
docker-compose up
```

### Swager UI
http://127.0.0.1:25566/api/v1/schema/swagger-ui/
