FROM python:3.13.0-slim

WORKDIR /backend
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /backend
EXPOSE 8080

CMD sh -c "flask db upgrade && flask --app backend run -h 0.0.0.0 -p $PORT"