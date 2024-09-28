import chromadb


model_name = "ai-forever/ru-en-RoSBERTa" # model_name = 'ai-forever/sbert_large_nlu_ru'
api_key = "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"

import chromadb.utils.embedding_functions as embedding_functions
huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=api_key,
    model_name=model_name
)


chroma_client = chromadb.HttpClient(host='87.242.119.60', port=8000)
print("DB ping Success")
