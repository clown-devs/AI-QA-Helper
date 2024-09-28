import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import pandas as pd
from ai.model import Model 
from fastapi.middleware.cors import CORSMiddleware

model = Model()

class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str
    class_1: str
    class_2: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"text": "Интеллектуальный помощник оператора службы поддержки."}

@app.post("/predict")
async def predict_sentiment(request: Request):
    answer = model.get_answer(request.question)
    response = Response(
        answer=answer,
        class_1="",
        class_2=""
    )
    return response

async def start_server():
    host = "0.0.0.0" # Сконфигурируйте host согласно настройкам вашего сервера.
    config = uvicorn.Config(app, host=host, port=8005)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    print("Server started...")
    asyncio.run(start_server())