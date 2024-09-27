# AI-QA-Helper
TODO: оформить документацию
Бот, созданный в рамках хакатона, нужен для *БЛА-БЛА-БЛА*

## Docker

#### Установка и запуск контейнеров
```bash
git clone https://github.com/clown-devs/AI-QA-Helper.git
cd AI-QA-Helper
docker compose up -d
```

## Backend

#### Установка зависимостей
> pip install -r requirements.txt

#### Запуск сервера
> python main.py

## Database

#### Создание векторизированного датасета
> python db/main.py
Создаст db/data директорию с векторным хранилищем

TODO: переписать на клиент-серверное взаимодействие БД (https://docs.trychroma.com/guides)