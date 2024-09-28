import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from embedding import HFEmbedding

chroma_client = chromadb.HttpClient(host='87.242.119.60', port=8000)

emedding_func = HFEmbedding()
collection = chroma_client.get_collection(
    name="rutube", 
    embedding_function=emedding_func
)


results = collection.query(
    query_texts=["Могу ли я загружать видео в формате MP5"], # Chroma will embed this for you
    n_results=3 # how many results to return
)
print(results)