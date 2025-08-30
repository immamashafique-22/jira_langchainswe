# LangChain SWE - Jira Integration

This project demonstrates integrating LangChain with Cohere embeddings to interact with Jira tickets.  
It allows you to fetch tickets, generate AI-powered summaries, create new tickets, and update existing ones.

## Features

- Fetch Jira tickets via API
- Generate summaries using Cohere embeddings
- Create new Jira tickets
- Update existing Jira tickets
- Uses LangChain for building the AI pipeline

## Setup

1. **Clone the repository**

```bash
git clone <repo-url>
cd jira_langchain


# Activate virtual environment

source venv/bin/activate  

# Install dependencies

pip install -r requirements.txt

# Run the project

python main.py
