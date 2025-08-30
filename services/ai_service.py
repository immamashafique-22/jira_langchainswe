from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import CohereEmbeddings
import os


class AIService:
    def __init__(self, documents):
        COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
        if not COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY environment variable not set!")
        self.embeddings = CohereEmbeddings(
            model="small", cohere_api_key=COHERE_API_KEY, user_agent="jira_langchain"
        )

        self.vectorstore = FAISS.from_texts(documents, self.embeddings)

    def retrieve(self, query, k=3):
        results = self.vectorstore.similarity_search(query, k=k)
        return [r.page_content for r in results]

    def get_summary(self, query):
        return "\n".join(self.retrieve(query))
