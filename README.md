# AI-QA-Helper

Интеллектуальный помощник оператора службы поддержки RuTube, который умеет генерировать ответы на основе базы знаний и классифицировать их.

Проект представляет собой тг-бота и web приложение, где оператор службы поддержки будет взаимодействовать с помощником. Модель обработает вопрос, сгенерирует ответ и произведет классификацию принадлежности вопроса бизнес логики процесса по уровню.

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

Создайте файл *.env* со следующей информацией в корне проекта:
```
CHROMA = "<your_db_host>"
CHROMA_PORT = "<your_db_port>"
HOST = "<your_api_host>"
PORT = "<your_api_port>"
TOKEN = "<your_bot_token>"
API = "<your_api_host>"
```

## Docker
### Запуск всех контейнеров
Чтобы backend запустился корректно, необходимо выполнить следующие действия:
```bash
docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
sudo apt-get purge -y nvidia-docker
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo pkill -SIGHUP dockerd
```

Запускаем все контейнеры (bot, frontend, backend. db):
```bash
cd AI-QA-Helper
docker compose up -d --build
```
### Отдельный запуск
#### Bot
```bash
cd AI-QA-Helper/bot
docker build -t 'bot'
docker run -d 'bot'
```
#### Backend
```bash
cd AI-QA-Helper/backend
docker build -t 'backend'
docker run -d 'backend'
```
### Frontend
```bash
cd AI-QA-Helper/frontend
docker build -t 'frontend'
docker run -d 'frontend'
```

### Database
```bash
cd AI-QA-Helper/db
docker build -t 'db'
docker run -d 'db'
```

## Использование

API для запросов находится по следующему адресу:
> https://clown-devs.ru/api/predict

Чтобы получить ответ от модели необходимо сделать POST запрос со следующим Json:
```json
{"question": "Ваш вопрос об RUTUBE"}
```

Тело ответа:
```json
{
    "answer": "Ваш ответ на RuTube",
    "class_1":"Классификатор 1",
    "class_1":"Классификатор 2"
}
```

### Swagger

Для получения swagger-документации можно перейти по адресу `https://clown-devs.ru/api/docs`