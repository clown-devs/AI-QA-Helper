import asyncio
import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import pandas as pd
from ai.model import Model 
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

model = Model()

class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str
    class_1: str
    class_2: str

app = FastAPI(
    servers=[
        {"url": "https://clown-devs.ru/api", "description": "Продовый сервер"},  
    ]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
index - ручка, которая возвращает приветственное сообщение для пользователя.
"""
@app.get("/", summary="Корневая ручка", description="Возвращает приветственное сообщение для пользователя.")
def index():
    return {"text": "Интеллектуальный помощник оператора службы поддержки."}

# Пример запроса: {"question": "Как загрузить видео на платформу Rutube?"}
"""
predict_sentiment - ручка, которая принимает запрос с вопросом о системе Rutube и ищет ответ на него в базе знаний.
"""
@app.post("/predict", summary="Предсказание ответа службы поддержки.", description="Принимает запрос с вопросом о системе Rutube и ищет ответ на него в базе знаний. Возвращает ответ на вопрос и 2 классификации вопроса.")
async def predict_sentiment(request: Request):
    if request.question[-1] != "?":
        request.question += "?"
    request.question = request.question[0].upper() + request.question[1:]

    answer = model.get_answer(request.question)
    class_1, class_2 = model.predict_class(request.question)
    if "не связан с платформой" in answer.lower():
        answer = "Данный вопрос не связан с платформой RuTube."
        class_1 = "ОТСУТСТВУЕТ"
        class_2 = "Отсутствует"
    answer = answer.replace("Данный вопрос связан с платформой RuTube.", "")    
    
    response = Response(
        answer=answer,
        class_1=class_1,
        class_2=class_2,
    )
    return response

async def start_server():
    load_dotenv()

    config = uvicorn.Config(app, host=str(os.getenv('HOST')), port=int(os.getenv('PORT')))
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    print("Server started...")
    asyncio.run(start_server())