import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from embedding import HFEmbeddingFunction

chroma_client = chromadb.HttpClient(host='87.242.119.60', port=8000)

emedding_func = HFEmbeddingFunction()
collection = chroma_client.get_collection(
    name="rutube", 
    embedding_function=emedding_func
)
import time
time_start = time.time()
results = collection.query(
    query_texts=["Могу ли я загружать видео в формате MP5"], 
    n_results=3 # сколько результатов вернуть
)
time_end = time.time()
print("MEASURE:",time_end - time_start)
print(results)