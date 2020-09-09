FROM python:3.8-slim

RUN apt-get update && apt-get install -y gcc libpq-dev

RUN pip install numpy pandas scipy matplotlib psycopg2

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app
VOLUME [ "/usr/src/app" ]
