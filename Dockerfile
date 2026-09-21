FROM python:3.11-slim

WORKDIR /app

# Copy application files
COPY backend /app/backend
COPY frontend /app/frontend

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

CMD ["python", "backend/app.py"]
