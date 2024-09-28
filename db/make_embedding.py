import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

import pandas as pd

# Считываем базу знаний
knowledge_base = pd.read_excel('baseline/rag/01_База_знаний.xlsx')
knowledge_base.rename(columns={'Вопрос из БЗ': 'question', 'Ответ из БЗ': 'answer'}, inplace=True)

# Считываем реальные кейсы использования
real_cases = pd.read_excel('baseline/rag/02_Реальные_кейсы.xlsx')
real_cases.rename(columns={'Вопрос пользователя': 'question', 'Ответ сотрудника': 'answer'}, inplace=True)

# Считываем эталонные вопросы-ответы из реальных кейсов
best_faq = pd.read_excel('baseline/rag/02_Реальные_кейсы.xlsx')
best_faq.rename(columns={'Вопрос из БЗ': 'question', 'Ответ из БЗ': 'answer'}, inplace=True)

# Объединяем все пары 'вопрос'-'ответ' из всех источников
data = pd.concat([
    knowledge_base[['question', 'answer']], 
    real_cases[['question', 'answer']], 
    best_faq[['question', 'answer']]
]).to_dict(orient='records');


def get_docs(data) -> Documents:
    documents = [f"Вопрос: {item['question']} Ответ: {item['answer']}" for item in data]
    return documents

def add_docs_to_collection(documents, collection):
    idx = 0
    for doc in documents:
        # Генерация уникального ID для каждого документа
        doc_id = f"doc_{idx}"
        idx += 1
        # Добавляем документ в коллекцию
        collection.add(
            ids=[doc_id],
            documents=[doc],
        )
        print("Added document:", doc_id)
    print("Documents added to collection")


class MyEmbeddingFunction(EmbeddingFunction):
    
    def __init__(self):
        from langchain_community.embeddings import HuggingFaceEmbeddings
        # Подключаем эмбеддинг модель
        model_name = "ai-forever/ru-en-RoSBERTa" # model_name = 'ai-forever/sbert_large_nlu_ru'
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}

        self.hf = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
    def __call__(self, input: Documents) -> Embeddings:
        # embed the documents somehow
        embeddings = self.hf.embed_documents(input)
        return embeddings
#---CHROMA---

emedding_func = MyEmbeddingFunction()
print("DB ping Success")
chroma_client = chromadb.HttpClient(host='87.242.119.60', port=8000)
chroma_client.delete_collection(name="rutube")
collection = chroma_client.get_or_create_collection(
    name="rutube", 
    embedding_function=emedding_func, 
    metadata={"hnsw:space": "cosine"}
)

print("Collection count:", collection.count())

documents = get_docs(data)
add_docs_to_collection(documents, collection)
print("Collection count:", collection.count())



