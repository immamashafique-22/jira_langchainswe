Sure! Below is a complete FastAPI application code along with pytest-based test cases based on the provided Jira ticket description.

### FastAPI Application Code

```python
# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define a model for the request body
class TestTicket(BaseModel):
    title: str
    description: str

@app.post("/tickets/")
async def create_ticket(ticket: TestTicket):
    """
    Create a new ticket.
    """
    if not ticket.title or not ticket.description:
        raise HTTPException(status_code=400, detail="Title and description are required.")
    
    # Here you would typically save the ticket to a database
    return {"message": "Ticket created successfully", "ticket": ticket}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Ticket API"}
```

### Pytest-based Test Cases

```python
# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Ticket API"}

def test_create_ticket_success():
    response = client.post(
        "/tickets/",
        json={"title": "Test Ticket via LangChain SWE", "description": "This ticket was created via LangChain SWE pipeline"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Ticket created successfully",
        "ticket": {
            "title": "Test Ticket via LangChain SWE",
            "description": "This ticket was created via LangChain SWE pipeline"
        }
    }

def test_create_ticket_missing_title():
    response = client.post(
        "/tickets/",
        json={"description": "This ticket was created via LangChain SWE pipeline"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Title and description are required."}

def test_create_ticket_missing_description():
    response = client.post(
        "/tickets/",
        json={"title": "Test Ticket via LangChain SWE"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Title and description are required."}
```

### Instructions to Run the Application and Tests

1. **Install FastAPI and Uvicorn**:
   Make sure you have FastAPI and Uvicorn installed. You can install them using pip:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the FastAPI Application**:
   You can run the FastAPI application using Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Install Pytest**:
   If you haven't installed pytest yet, you can do so with:
   ```bash
   pip install pytest
   ```

4. **Run the Tests**:
   You can run the tests using pytest:
   ```bash
   pytest tests/test_main.py
   ```

This setup provides a simple FastAPI application that handles ticket creation and includes unit tests to verify its functionality. Adjust the code as necessary to fit your specific requirements or environment.