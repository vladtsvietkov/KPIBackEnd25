FROM python:3.13.0-slim

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /app

CMD flask --app api run -h 0.0.0.0 -p $PORT