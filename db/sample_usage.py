import chromadb.utils.embedding_functions as embedding_functions
import chromadb

model_name = "ai-forever/ru-en-RoSBERTa" # model_name = 'ai-forever/sbert_large_nlu_ru'
api_key = "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"

import chromadb.utils.embedding_functions as embedding_functions
huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=api_key,
    model_name=model_name
)


# Функция для поиска топ-N ближайших документов
def get_top_k_similar_docs(user_question: str, collection, top_k=5):

    # Поиск ближайших векторов в коллекции
    results = collection.query(
        query_texts=[user_question],  # Текст запроса
        n_results=top_k  # Количество результатов
    )

    return results


# Инициализируем клиент бдшки
chroma_client = chromadb.HttpClient(host='87.242.119.60', port=8000)

# получаем коллекцию векторов, которая называется "rutube"
# коллекция - аналог таблицы в СУБД
collection = chroma_client.get_collection(name="rutube", embedding_function=huggingface_ef)
print("Collection count:", collection.count())
#Пример использования
user_question = "Могу ли я загружать видео в формате MP5"
top_5_results = get_top_k_similar_docs(user_question, collection, top_k=5)

# Печатаем результаты
for idx, result in enumerate(top_5_results['documents']):
    print(f"Результат {idx+1}: {result}")