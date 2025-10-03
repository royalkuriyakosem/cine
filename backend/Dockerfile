# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Run migrations before starting the server
CMD ["sh", "-c", "python manage.py migrate && gunicorn filmhub.wsgi:application --bind 0.0.0.0:8000"]
