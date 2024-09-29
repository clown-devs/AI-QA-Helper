FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /AI-QA-Helper

RUN pip install --upgrade pip
COPY ./backend/requirements.txt /AI-QA-Helper/
COPY ./backend/.env /AI-QA-Helper/backend/
COPY ./ai/.env /AI-QA-Helper/ai/
RUN pip install -r requirements.txt
COPY . .