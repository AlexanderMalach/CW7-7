FROM python:3.12-slim


# Установить зависимости Python
WORKDIR /app
COPY /requirements.txt /
RUN pip install -r /requirements.txt --no-cache-dir

# Скопировать исходный код
COPY . .

# # CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]