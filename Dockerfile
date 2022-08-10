FROM python:3.10

WORKDIR /99app

COPY ./user-service/requirements.txt .

RUN pip install -r requirements.txt

COPY ./user-service ./user-service

CMD [ "python", "./user-service/app.py" ]