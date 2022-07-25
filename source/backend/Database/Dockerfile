FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

<<<<<<< HEAD:source/backend/Database/Dockerfile
COPY database.py /code/app/database.py
=======
COPY ./source/backend /code/app

# CMD ["uvicorn", "app.server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 94e24d59b9250cd5e64f0b635e4c6c98b08c4daf:Dockerfile
EXPOSE 27017
