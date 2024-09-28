from chromadb import Documents, EmbeddingFunction, Embeddings
import pandas as pd
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

    ]).to_dict(orient='records');

    return get_docs(data)

def get_docs(data):
    documents = [f"Вопрос: {item['question']} Ответ: {item['answer']}" for item in data]
    class1 = [item['class1'] for item in data]
    class2 = [item['class2'] for item in data]
    return documents, class1, class2