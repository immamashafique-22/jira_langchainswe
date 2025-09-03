To implement a Jira to GitHub sync pipeline using FastAPI, we will create a simple FastAPI application that listens for webhooks from Jira and then creates or updates issues in GitHub accordingly. Below is the complete FastAPI app code along with the unit tests using Pytest.

### FastAPI Application Code

```python
# app/main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
GITHUB_BASE_URL = os.getenv("GITHUB_BASE_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

@app.post("/webhook/jira")
async def jira_webhook(request: Request):
    try:
        payload = await request.json()
        issue_key = payload.get("issue", {}).get("key")
        issue_summary = payload.get("issue", {}).get("fields", {}).get("summary")
        issue_status = payload.get("issue", {}).get("fields", {}).get("status", {}).get("name")

        if not issue_key or not issue_summary:
            raise HTTPException(status_code=400, detail="Invalid payload")

        # Create or update GitHub issue
        github_issue_url = f"{GITHUB_BASE_URL}/repos/{GITHUB_REPO}/issues"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Check if the issue already exists in GitHub
        async with httpx.AsyncClient() as client:
            response = await client.get(github_issue_url, headers=headers)
            response.raise_for_status()
            issues = response.json()

            # Check if the issue already exists
            existing_issue = next((issue for issue in issues if issue["title"] == issue_summary), None)

            if existing_issue:
                # Update existing issue
                update_url = f"{github_issue_url}/{existing_issue['number']}"
                await client.patch(update_url, headers=headers, json={"state": issue_status})
            else:
                # Create new issue
                await client.post(github_issue_url, headers=headers, json={
                    "title": issue_summary,
                    "body": f"Jira Issue: {issue_key}\nStatus: {issue_status}",
                    "state": issue_status
                })

        return JSONResponse(content={"message": "Sync successful"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

```

### Unit Tests with Pytest

```python
# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_jira_payload():
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

def test_jira_webhook_success(mock_jira_payload, monkeypatch):
    # Mock the GitHub API responses
    async def mock_get(*args, **kwargs):
        return {"json": lambda: [{"title": "Test issue", "number": 1}]}

    async def mock_post(*args, **kwargs):
        return {"json": lambda: {"number": 2}}

    async def mock_patch(*args, **kwargs):
        return {"json": lambda: {}}

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)
    monkeypatch.setattr("httpx.AsyncClient.post", mock_post)
    monkeypatch.setattr("httpx.AsyncClient.patch", mock_patch)

    response = client.post("/webhook/jira", json=mock_jira_payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Sync successful"}

def test_jira_webhook_invalid_payload():
    response = client.post("/webhook/jira", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid payload"}

def test_jira_webhook_exception(monkeypatch):
    async def mock_get(*args, **kwargs):
        raise Exception("GitHub API error")

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    response = client.post("/webhook/jira", json={"issue": {"key": "JIRA-123"}})
    assert response.status_code == 500
    assert response.json() == {"detail": "GitHub API error"}
```

### Environment Variables

Make sure to set the following environment variables before running the application:

- `JIRA_BASE_URL`: The base URL for your Jira instance.
- `GITHUB_BASE_URL`: The base URL for the GitHub API (usually `https://api.github.com`).
- `GITHUB_TOKEN`: A personal access token for GitHub with the necessary permissions to create and update issues.
- `GITHUB_REPO`: The repository in the format `owner/repo`.

### Running the Application

To run the FastAPI application, use the command:

```bash
uvicorn app.main:app --reload
```

### Running the Tests

To run the tests, use the command:

```bash
pytest tests/
```

This setup provides a basic implementation of a Jira to GitHub sync pipeline using FastAPI, along with unit tests to ensure functionality. Adjust the logic as necessary to fit your specific requirements.