To implement a Jira to GitHub sync pipeline using FastAPI, we will create a simple FastAPI application that listens for webhooks from Jira and GitHub. The application will handle the synchronization of issues between the two platforms.

### FastAPI Application Code

Here is a complete FastAPI application code that implements the Jira to GitHub sync pipeline:

```python
# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@app.post("/jira-webhook/")
async def jira_webhook(request: Request):
    try:
        payload = await request.json()
        issue_key = payload['issue']['key']
        issue_summary = payload['issue']['fields']['summary']
        issue_status = payload['issue']['fields']['status']['name']

        # Create or update GitHub issue
        await sync_with_github(issue_key, issue_summary, issue_status)
        return JSONResponse(content={"message": "Sync successful"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def sync_with_github(issue_key: str, issue_summary: str, issue_status: str):
    async with httpx.AsyncClient() as client:
        # Check if the issue already exists in GitHub
        response = await client.get(f"https://api.github.com/repos/{GITHUB_REPO}/issues", headers={
            "Authorization": f"token {GITHUB_TOKEN}"
        })
        response.raise_for_status()
        issues = response.json()

        # Check if the issue already exists
        existing_issue = next((issue for issue in issues if issue_key in issue['title']), None)

        if existing_issue:
            # Update existing issue
            await client.patch(f"https://api.github.com/repos/{GITHUB_REPO}/issues/{existing_issue['number']}", json={
                "state": issue_status.lower(),
                "body": f"Jira Issue: {issue_key}\nSummary: {issue_summary}\nStatus: {issue_status}"
            }, headers={
                "Authorization": f"token {GITHUB_TOKEN}"
            })
        else:
            # Create new issue
            await client.post(f"https://api.github.com/repos/{GITHUB_REPO}/issues", json={
                "title": f"{issue_key}: {issue_summary}",
                "body": f"Jira Issue: {issue_key}\nSummary: {issue_summary}\nStatus: {issue_status}"
            }, headers={
                "Authorization": f"token {GITHUB_TOKEN}"
            })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Unit Tests with Pytest

Here are the unit tests for the FastAPI application using Pytest:

```python
# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def mock_jira_webhook_payload():
    return {
        "issue": {
            "key": "JIRA-123",
            "fields": {
                "summary": "Test issue",
                "status": {
                    "name": "In Progress"
                }
            }
        }
    }

def test_jira_webhook_success(mock_jira_webhook_payload, monkeypatch):
    async def mock_sync_with_github(issue_key, issue_summary, issue_status):
        return

    monkeypatch.setattr("main.sync_with_github", mock_sync_with_github)

    response = client.post("/jira-webhook/", json=mock_jira_webhook_payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Sync successful"}

def test_jira_webhook_failure(monkeypatch):
    async def mock_sync_with_github(issue_key, issue_summary, issue_status):
        raise Exception("Sync failed")

    monkeypatch.setattr("main.sync_with_github", mock_sync_with_github)

    response = client.post("/jira-webhook/", json={})
    assert response.status_code == 400
    assert "detail" in response.json()
```

### Instructions to Run the Application

1. **Install Dependencies**: Make sure you have FastAPI and httpx installed. You can install them using pip:

   ```bash
   pip install fastapi uvicorn httpx pytest
   ```

2. **Set Environment Variables**: Set the following environment variables before running the application:

   ```bash
   export JIRA_BASE_URL="https://your-jira-instance.atlassian.net"
   export GITHUB_REPO="yourusername/yourrepo"
   export GITHUB_TOKEN="your_github_token"
   ```

3. **Run the Application**: Start the FastAPI application using Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```

4. **Run Tests**: You can run the tests using pytest:

   ```bash
   pytest test_main.py
   ```

This setup provides a basic implementation of a Jira to GitHub sync pipeline using FastAPI, along with unit tests to ensure the functionality works as expected.