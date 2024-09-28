import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from embedding import HFEmbeddingFunction
import pandas as pd

# get_samples функция для получения сэмплов вопросов-ответов
# возвращает 3 массива: конкатенированные вопрос-ответы, классификатор1 и классификатор2
def get_samples():
    # Считываем базу знаний
    knowledge_base = pd.read_excel('baseline/rag/01_База_знаний.xlsx')
    knowledge_base.rename(columns={'Вопрос из БЗ': 'question', 'Ответ из БЗ': 'answer', 'Классификатор 1 уровня': 'class1', 'Классификатор 2 уровня': 'class2'}, inplace=True)

    # Считываем реальные кейсы использования
    real_cases = pd.read_excel('baseline/rag/02_Реальные_кейсы.xlsx')
    real_cases.rename(columns={'Вопрос пользователя': 'question', 'Ответ сотрудника': 'answer', 'Классификатор 1 уровня': 'class1', 'Классификатор 2 уровня': 'class2'}, inplace=True)

    # Считываем эталонные вопросы-ответы из реальных кейсов
    best_faq = pd.read_excel('baseline/rag/02_Реальные_кейсы.xlsx')
    best_faq.rename(columns={'Вопрос из БЗ': 'question', 'Ответ из БЗ': 'answer', 'Классификатор 1 уровня': 'class1', 'Классификатор 2 уровня': 'class2'}, inplace=True)

    # Объединяем все пары 'вопрос'-'ответ' из всех источников
    data = pd.concat([
        knowledge_base[['question', 'answer', 'class1', 'class2']], 
        real_cases[['question', 'answer', 'class1', 'class2']], 
        best_faq[['question', 'answer', 'class1', 'class2']]

    ])
    data = data.drop_duplicates(subset=data.columns).to_dict(orient='records')
    return get_docs(data)

def get_docs(data):
    documents = [f"Вопрос: {item['question']} Ответ: {item['answer']}" for item in data]
    class1 = [item['class1'] for item in data]
    class2 = [item['class2'] for item in data]
    return documents, class1, class2
    
def add_docs_to_collection(documents, class1, class2, collection):
    for i in range(len(documents)):
        # Генерация уникального ID для каждого документа
        doc_id = f"doc_{i}"
        
        # Добавляем документ в коллекцию
        collection.add(
            ids=[doc_id],
            documents=[documents[i]],
            metadatas=[{"class1": class1[i], "class2":class2[i]}]
        )
        print("Added document:", doc_id)
        print(documents[i])
        print(class1[i])
        print(class2[i])
        print('-------')
    print("Documents added to collection")



emedding_func = HFEmbeddingFunction()
chroma_client = chromadb.HttpClient(host='87.242.119.60', port=8000)
chroma_client.delete_collection(name="rutube")
collection = chroma_client.get_or_create_collection(
    name="rutube", 
    embedding_function=emedding_func, 
    metadata={"hnsw:space": "cosine"}
)

print("Collection count:", collection.count())

documents, class1, class2 = get_samples()
add_docs_to_collection(documents, class1, class2,  collection)
print("Collection count:", collection.count())



