FROM python:3.10-alpine
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./source/backend /code/app
EXPOSE 27017

WORKDIR /code/app/Database
