FROM python:3.12-slim

WORKDIR /app/services/governance-service
ENV PYTHONPATH=/app

COPY backend /app/backend
COPY services/governance-service /app/services/governance-service
COPY backend/pyproject.toml /app/backend/pyproject.toml

RUN pip install --no-cache-dir /app/backend

EXPOSE 8103
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8103"]
