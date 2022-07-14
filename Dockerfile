FROM python:3.10


RUN mkdir app
WORKDIR /app

# System Dependencies
RUN apt-get update && apt-get install -y bash gcc libc-dev make libffi-dev python3-dev librdkafka-dev

# App dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY gunicorn.conf.py .
COPY api /app/api
