import chromadb
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from db.embedding import HFEmbeddingFunction
from langchain_core.output_parsers import StrOutputParser

model_name_llm = "microsoft/Phi-3.5-mini-instruct"

def load_model():
    model = AutoModelForCausalLM.from_pretrained(
    model_name_llm,
    device_map="cuda", 
    torch_dtype="auto", 
    trust_remote_code=True, 
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name_llm)
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )
    generation_args = {
        "max_new_tokens": 700,
        "return_full_text": False,
        "temperature": 0.6,
        "do_sample":True
        #"top_p":0.4,
    }
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, **generation_args)
    llm = HuggingFacePipeline(pipeline=pipe)

    return ChatHuggingFace(llm=llm,  tokenizer=tokenizer)

def get_collection():
    chroma_client = chromadb.HttpClient(host='87.242.119.60', port=8000)

    emedding_func = HFEmbeddingFunction()
    collection = chroma_client.get_collection(
        name="rutube", 
        embedding_function=emedding_func
    )
    return collection

from langchain.schema import BaseRetriever, Document
class CustomRetriever(BaseRetriever):
    collection: chromadb.Collection
    def __init__(self, collection):
        super().__init__(collection=collection)
    def _get_relevant_documents(self, query: str):
        results = self.collection.query(query_texts=[query], n_results=3)  # Пример вызова к источнику данных\
        documents = [Document(page_content=result) for result in results['documents'][0]]
        return documents

def create_chain(model, collection):
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', """Ты — интелектуальный помощник оператора службы поддержки Rutube, который отвечает на вопросы о поддержке. 
            Для ответа на вопрос ты должен использовать только информацию из контекста.
            Отвечай НА РУССКОМ ЯЗЫКЕ.
            Контекст: {context} """),
            ('user', "Вопрос: {question}")
        ]
    )
    retriever = CustomRetriever(collection)
    # Извлечение контекста
    context = retriever | RunnablePassthrough()

    rag_chain = (
        {"context": context, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )   
    return rag_chain

def invoke_model(chain, query):
    response = chain.invoke(query)
    return response

class Model():
    def __init__(self):
        self.chat_model = load_model()
        self.collection = get_collection()
        self.chain = create_chain(self.chat_model, self.collection)

    def get_answer(self, question: str) -> str:
        return invoke_model(self.chain, question)



