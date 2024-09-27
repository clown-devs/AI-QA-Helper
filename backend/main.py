import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import pandas as pd

# считаем базу Часто задаваемых вопросов RUTUBE 
faq = pd.read_excel("baseline/rag/01_База_знаний.xlsx")
faq.head()
# С помощью модели извлечения embbeddings из текста получим embbeddings для всех вопросов из FAQ.
# Веса модели можно найти по ссылке: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
faq_embeddings = model.encode(faq['Вопрос из БЗ'].values)

class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str
    class_1: str
    class_2: str

app = FastAPI()

@app.get("/")
def index():
    return {"text": "Интеллектуальный помощник оператора службы поддержки."}

@app.post("/predict")
async def predict_sentiment(request: Request):
    question_embedding = model.encode(request.question)
    similarities = cos_sim(question_embedding, faq_embeddings)
    anwer_data = faq.iloc[similarities.argmax().item()]
    response = Response(
        answer=anwer_data['Ответ из БЗ'],
        class_1=anwer_data['Классификатор 1 уровня'], # Классификатор оценивается опционально; при отсутствии можно задать константное значение.
        class_2=anwer_data['Классификатор 2 уровня'], # Классификатор оценивается опционально; при отсутствии можно задать константное значение.
    )
    return response

async def start_server():
    host = "0.0.0.0" # Сконфигурируйте host согласно настройкам вашего сервера.
    config = uvicorn.Config(app, host=host, port=8000)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    print("Server started...")
    asyncio.run(start_server())