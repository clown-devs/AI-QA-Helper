# AI-QA-Helper
TODO: оформить документацию
Бот, созданный в рамках хакатона, нужен для *БЛА-БЛА-БЛА*

## Получение репозитория
```bash
git clone https://github.com/clown-devs/AI-QA-Helper.git
```

## HTTPS
Frontend использует защищенное соединение https, если вы не хотите использовать шифрование, измените файл **./frontend/nginx.conf**, иначе создайте сертификат letsencrypt.

Если у вас уже работает nginx на 80 порту, отключите его на время получения сертификата:
> sudo systemctl stop nginx

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d <yourdomain.com>
```

Включите nginx, если необходимо:
> sudo systemctl start nginx

Переместите созданные ключи в директорию *frontend* и измените права доступа:
```bash
sudo mv /etc/letsencrypt/live/<yourdomain.com>/fullchain.pem ~/AI-QA-Helper/frontend/
sudo mv /etc/letsencrypt/live/<yourdomain.com>/privkey.pem ~/AI-QA-Helper/frontend/
sudo chmod o+rx ~/AI-QA-Helper/frontend/fullchain.pem
sudo chmod o+rx ~/AI-QA-Helper/frontend/privkey.pem
```

## Docker
### Запуск всех контейнеров
```bash
cd AI-QA-Helper
docker compose up -d
```
### Отдельный запуск
#### bot
```bash
cd AI-QA-Helper/bot
docker build -t 'bot'
docker run -d 'bot'
```
#### backend
```bash
cd AI-QA-Helper/backend
docker build -t 'backend'
docker run -d 'backend'
```
### frontend
```bash
cd AI-QA-Helper/frontend
docker build -t 'frontend'
docker run -d 'frontend'
```


## Ручной запуск

### backend

#### Установка зависимостей
> pip install -r requirements.txt

#### Запуск сервера
> python main.py

### Database

#### Создание векторизированного датасета
> python db/main.py
Создаст db/data директорию с векторным хранилищем

TODO: переписать на клиент-серверное взаимодействие БД (https://docs.trychroma.com/guides)