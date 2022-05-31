FROM python:3.10-alpine


RUN mkdir app
WORKDIR /app

# System Dependencies
RUN apk update && apk add build-base bash gcc libc-dev make libffi-dev openssl-dev python3-dev

# App dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY gunicorn.conf.py .
COPY api /app/api

# Entry point
CMD ["gunicorn", "api.main:app"]
