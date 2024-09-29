import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from embedding import HFEmbeddingFunction

# Скрипт демонстрирует пример использования базы данных ChromaDB

chroma_client = chromadb.HttpClient(host='87.242.119.60', port=8000)

emedding_func = HFEmbeddingFunction()
collection = chroma_client.get_collection(
    name="rutube", 
    embedding_function=emedding_func
)

results = collection.query(
    query_texts=["Могу ли я загружать видео в формате MP5"], 
    n_results=3 # сколько результатов вернуть
)

print(results)