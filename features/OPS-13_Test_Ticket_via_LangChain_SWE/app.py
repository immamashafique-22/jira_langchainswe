Sure! Below is a complete FastAPI application code along with pytest-based test cases based on the provided Jira ticket description.

### FastAPI Application Code

```python
# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Model for the request body
class TestTicket(BaseModel):
    title: str
    description: str

# Endpoint to create a test ticket
@app.post("/tickets/", response_model=TestTicket)
async def create_ticket(ticket: TestTicket):
    if not ticket.title or not ticket.description:
        raise HTTPException(status_code=400, detail="Title and description are required")
    return ticket

# Endpoint to get a test ticket (for demonstration purposes)
@app.get("/tickets/{ticket_id}", response_model=TestTicket)
async def get_ticket(ticket_id: int):
    # For demonstration, we will return a static ticket
    if ticket_id != 1:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TestTicket(title="Test Ticket via LangChain SWE", description="This ticket was created via LangChain SWE pipeline")
```

### Pytest-Based Test Cases

```python
# test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_create_ticket_success():
    response = client.post("/tickets/", json={"title": "Test Ticket", "description": "This is a test ticket."})
    assert response.status_code == 200
    assert response.json() == {"title": "Test Ticket", "description": "This is a test ticket."}

def test_create_ticket_missing_title():
    response = client.post("/tickets/", json={"description": "This is a test ticket."})
    assert response.status_code == 400
    assert response.json() == {"detail": "Title and description are required"}

def test_create_ticket_missing_description():
    response = client.post("/tickets/", json={"title": "Test Ticket"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Title and description are required"}

def test_get_ticket_success():
    response = client.get("/tickets/1")
    assert response.status_code == 200
    assert response.json() == {"title": "Test Ticket via LangChain SWE", "description": "This ticket was created via LangChain SWE pipeline"}

def test_get_ticket_not_found():
    response = client.get("/tickets/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}
```

### Instructions to Run the Application and Tests

1. **Install FastAPI and Uvicorn**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the FastAPI Application**:
   ```bash
   uvicorn app:app --reload
   ```

3. **Install Pytest**:
   ```bash
   pip install pytest
   ```

4. **Run the Tests**:
   ```bash
   pytest test_app.py
   ```

This setup provides a simple FastAPI application with endpoints to create and retrieve tickets, along with corresponding unit tests to verify the functionality. Adjust the application logic as necessary to fit your specific requirements.