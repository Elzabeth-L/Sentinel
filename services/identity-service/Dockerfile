FROM python:3.12-slim

WORKDIR /app/services/identity-service
ENV PYTHONPATH=/app

COPY backend /app/backend
COPY services/identity-service /app/services/identity-service
COPY backend/pyproject.toml /app/backend/pyproject.toml

RUN pip install --no-cache-dir /app/backend

EXPOSE 8101
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8101"]
