import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from embedding import HFEmbeddingFunction, get_samples

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



