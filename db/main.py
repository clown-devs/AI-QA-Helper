import chromadb
import pandas as pd

# считаем базу Часто задаваемых вопросов RUTUBE 
faq = pd.read_excel("baseline/rag/01_База_знаний.xlsx")
faq.head()

# Генерация эмбеддингов для вопросов
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
faq_embeddings = model.encode(faq['Вопрос из БЗ'].values)

# Создание уникальных идентификаторов для каждого вопроса
ids = [f"faq_{i}" for i in range(len(faq))]

# Инициализация клиента
client = chromadb.PersistentClient(path="db/data")

# Создание коллекции (например, база знаний)
knowledge_base = client.create_collection("my_knowledge_base")

# Добавление эмбеддингов в базу данных
knowledge_base.add(
    ids=ids,  # идентификаторы
    embeddings=faq_embeddings.tolist(),  # преобразуем эмбеддинги в список
    documents=faq['Вопрос из БЗ'].values.tolist()  # исходные тексты вопросов
)

