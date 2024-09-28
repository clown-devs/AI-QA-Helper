FROM python:3.11-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /TG_Bot

RUN pip install --upgrade pip
COPY ./bot/requirements.txt /TG_Bot/
COPY ./bot/.env /TG_Bot/
RUN pip install -r requirements.txt
COPY . .