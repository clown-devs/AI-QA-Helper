from chromadb import Documents, EmbeddingFunction, Embeddings

"""
HFEmbeddingFunction - это класс, который используется для создания эмбеддингов текста с помощью HuggingFace модели.
"""
class HFEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        from langchain_community.embeddings import HuggingFaceEmbeddings
        # Подключаем эмбеддинг модель
        model_name = "ai-forever/ru-en-RoSBERTa" # model_name = 'ai-forever/sbert_large_nlu_ru'
        model_kwargs = {'device': 'cuda'}
        encode_kwargs = {'normalize_embeddings': False}

        self.hf = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = self.hf.embed_documents(input)
        return embeddings
