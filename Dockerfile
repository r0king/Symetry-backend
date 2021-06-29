FROM python:3.9.2-slim

COPY ./app /app

COPY ./test.py test.py

COPY  ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD [ "python", "test.py" ]