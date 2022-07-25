FROM python:3.10-alpine
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY database.py /code/app/database.py
EXPOSE 27017
