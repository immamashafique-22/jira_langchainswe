Certainly! Below is a complete FastAPI application that implements a Jira to GitHub sync pipeline, along with unit tests using Pytest.

### FastAPI Application Code

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Configuration for Jira and GitHub
JIRA_URL = os.getenv("JIRA_URL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
GITHUB_URL = os.getenv("GITHUB_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class JiraIssue(BaseModel):
    key: str
    title: str
    description: str

@app.post("/sync")
async def sync_jira_to_github(issue: JiraIssue):
    # Fetch the issue from Jira
    jira_issue = fetch_jira_issue(issue.key)
    if not jira_issue:
        raise HTTPException(status_code=404, detail="Jira issue not found")

    # Create a corresponding GitHub issue
    github_issue = create_github_issue(issue.title, jira_issue['fields']['description'])
    return {"message": "Issue synced successfully", "github_issue": github_issue}

def fetch_jira_issue(issue_key: str):
    response = requests.get(
        f"{JIRA_URL}/rest/api/2/issue/{issue_key}",
        auth=('', JIRA_API_TOKEN)
    )
    if response.status_code == 200:
        return response.json()
    return None

def create_github_issue(title: str, body: str):
    response = requests.post(
        f"{GITHUB_URL}/repos/your_username/your_repo/issues",
        json={"title": title, "body": body},
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    if response.status_code == 201:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail="Failed to create GitHub issue")
```

### Unit Tests with Pytest

```python
# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def mock_jira_issue(monkeypatch):
    def mock_fetch_jira_issue(issue_key):
        return {
            "fields": {
                "description": "This is a test issue description."
            }
        }
    
    monkeypatch.setattr("main.fetch_jira_issue", mock_fetch_jira_issue)

@pytest.fixture
def mock_create_github_issue(monkeypatch):
    def mock_create_github_issue(title, body):
        return {
            "html_url": "https://github.com/your_username/your_repo/issues/1",
            "title": title,
            "body": body
        }
    
    monkeypatch.setattr("main.create_github_issue", mock_create_github_issue)

def test_sync_jira_to_github(mock_jira_issue, mock_create_github_issue):
    response = client.post("/sync", json={"key": "TEST-1", "title": "Test Issue", "description": "This is a test issue."})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Issue synced successfully",
        "github_issue": {
            "html_url": "https://github.com/your_username/your_repo/issues/1",
            "title": "Test Issue",
            "body": "This is a test issue description."
        }
    }

def test_sync_jira_to_github_issue_not_found():
    response = client.post("/sync", json={"key": "INVALID-1", "title": "Invalid Issue", "description": "This issue does not exist."})
    assert response.status_code == 404
    assert response.json() == {"detail": "Jira issue not found"}

def test_create_github_issue_failure(mock_jira_issue):
    # Simulate a failure in creating a GitHub issue
    def mock_create_github_issue_failure(title, body):
        raise HTTPException(status_code=500, detail="Failed to create GitHub issue")
    
    with pytest.raises(HTTPException):
        client.post("/sync", json={"key": "TEST-1", "title": "Test Issue", "description": "This is a test issue."})
```

### Instructions for Running the Application and Tests

1. **Environment Variables**: Make sure to set the following environment variables before running the application:
   - `JIRA_URL`: The base URL for your Jira instance.
   - `JIRA_API_TOKEN`: Your Jira API token.
   - `GITHUB_URL`: The base URL for your GitHub repository (e.g., `https://api.github.com`).
   - `GITHUB_TOKEN`: Your GitHub personal access token.

2. **Install Dependencies**: You need to install FastAPI and the required libraries. You can do this using pip:
   ```bash
   pip install fastapi[all] requests pytest
   ```

3. **Run the Application**: You can run the FastAPI application using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

4. **Run the Tests**: To run the tests, use the following command:
   ```bash
   pytest test_main.py
   ```

This setup provides a basic structure for syncing Jira issues to GitHub issues, along with unit tests to ensure the functionality works as expected. Adjust the GitHub repository URL and other configurations as necessary for your specific use case.