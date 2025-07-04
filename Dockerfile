# Use the official slim Python base image
FROM python:3.12-slim

WORKDIR /app

# (better for Docker layer caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
