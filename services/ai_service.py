# services/ai_service.py
from langchain_cohere import ChatCohere
from langchain_cohere.embeddings import CohereEmbeddings
import json
import os


class LangChainAIService:
    def __init__(self, docs: list[str]):
        """
        Initialize AI service with documents (Jira tickets).
        """
        # Embeddings
        self.embeddings = CohereEmbeddings(
            cohere_api_key=os.environ.get("COHERE_API_KEY"),
            model="embed-english-v3.0",
        )

        # Chat LLM (use ChatCohere instead of Cohere)
        self.llm = ChatCohere(
            cohere_api_key=os.environ.get("COHERE_API_KEY"),
            model="command-r",
            temperature=0,
            max_tokens=300,
        )

        self.docs = docs

    def summarize_tickets(self) -> str:
        docs_text = "\n".join(self.docs)
        prompt = f"""
Summarize these Jira tickets and suggest priorities:

{docs_text}
"""
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    def generate_pr_suggestions(self, ticket: dict) -> dict:
        prompt = f"""
You are an AI assistant. Generate a GitHub pull request suggestion for this Jira ticket:

Ticket Key: {ticket['key']}
Summary: {ticket['summary']}
Description: {ticket['description']}

Return ONLY a JSON object with:
- branch
- title
- description
- files: dict of {{filename: content}}
"""
        response = self.llm.invoke(prompt)
        text = response.content if hasattr(response, "content") else str(response)

        try:
            pr_data = json.loads(text)
        except Exception:
            pr_data = {
                "branch": f"{ticket['key']}-branch",
                "title": f"PR for {ticket['key']}",
                "description": ticket["summary"],
                "files": {"README.md": f"# Update for {ticket['key']}"},
            }
        return pr_data
