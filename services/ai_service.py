from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.llms import Cohere
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os


class LangChainAIService:
    def __init__(self, documents):
        COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
        if not COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY environment variable not set!")

        self.embeddings = CohereEmbeddings(
            model="small",
            cohere_api_key=COHERE_API_KEY,
            user_agent="langchainSWE-jira_project/1.0",
        )

        self.vectorstore = FAISS.from_texts(documents, self.embeddings)

        self.llm = Cohere(
            model="command",
            cohere_api_key=COHERE_API_KEY,
            temperature=0.5,
            max_tokens=300,
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            return_source_documents=False,
            chain_type_kwargs={
                "prompt": PromptTemplate(
                    template="Summarize the following Jira tickets and suggest priority: {context}\nAnswer concisely.",
                    input_variables=["context"],
                )
            },
        )

    def summarize_tickets(
        self, query="Summarize key issues and suggest tickets to prioritize."
    ):
        return self.qa_chain.invoke({"query": query})
