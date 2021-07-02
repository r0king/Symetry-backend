FROM python:3.9.2-slim

COPY ./app /app

COPY  ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /app

CMD [ "uvicorn", "app.main:app", "--reload", "--port", "80", "--host", "0.0.0.0"]
