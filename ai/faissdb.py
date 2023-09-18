from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

class FAISSDB:
    def __init__(self, apikey):
        self._apikey = apikey

    def get_context(self, query):
        # Load db from database
        embeddings = OpenAIEmbeddings(openai_api_key=self._apikey)
        loaded_db = FAISS.load_local("/app/actions/rasa_indexes/resume_faiss_index", embeddings)

        with open('/app/actions/log.txt', 'a') as log:
            log.write(f'QUERY: {str(query)}\n')
            docs_and_scores = loaded_db.similarity_search_with_score(str(query), k = 8)
            context = ''
            for doc in docs_and_scores:
                if doc[1] < 0.5:
                    context += doc[0].page_content + "\n"
            log.write(f'CONTEXT: {context}')
        
        return context