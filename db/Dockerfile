FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /DB

RUN pip install --upgrade pip
COPY ./requirements.txt /DB/
RUN pip install -r requirements.txt
COPY . .