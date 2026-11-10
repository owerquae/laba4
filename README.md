# Django Record App (Docker + PostgreSQL)

## Запуск проекта
1. Убедитесь, что у вас установлен Docker и Docker Compose.
2. Создайте файл `.env` в корне проекта (рядом с `manage.py`) и заполните его:
   ```env
   POSTGRES_DB=mydb
   POSTGRES_USER=myuser
   POSTGRES_PASSWORD=supersecret123
   POSTGRES_HOST=db
   POSTGRES_PORT=5432