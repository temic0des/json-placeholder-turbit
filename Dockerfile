# syntax=docker/dockerfile:1
FROM python:3.10

WORKDIR /json-placeholder

COPY ./requirements.txt /json-placeholder/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /json-placeholder/requirements.txt

COPY ./app /json-placeholder/app

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]