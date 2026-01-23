FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py makemigrations app && python manage.py migrate && python manage.py popular_dados --verbosity=0 && python manage.py runserver 0.0.0.0:8000"]