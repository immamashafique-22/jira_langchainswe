import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Jira configuration
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_SERVER = os.getenv("JIRA_SERVER")
PROJECT_KEY = os.getenv("PROJECT_KEY")

# OpenAI configuration (optional, if you have a key)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Cohere configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY")


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
