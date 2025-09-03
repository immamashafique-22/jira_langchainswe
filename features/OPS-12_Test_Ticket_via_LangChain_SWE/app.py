Sure! Below is a complete FastAPI application code along with pytest-based unit tests based on the provided Jira ticket description.

### FastAPI Application Code

```python
# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Model for the request body
class Ticket(BaseModel):
    title: str
    description: str

# In-memory storage for tickets
tickets_db = []

@app.post("/tickets/", response_model=Ticket)
async def create_ticket(ticket: Ticket):
    tickets_db.append(ticket)
    return ticket

@app.get("/tickets/", response_model=List[Ticket])
async def get_tickets():
    return tickets_db

@app.get("/")
async def root():
    return {"message": "Welcome to the Ticket API!"}
```

### Pytest Unit Tests

```python
# test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app, Ticket

client = TestClient(app)

def test_create_ticket():
    response = client.post("/tickets/", json={"title": "Test Ticket via LangChain SWE", "description": "This ticket was created via LangChain SWE pipeline"})
    assert response.status_code == 200
    assert response.json() == {"title": "Test Ticket via LangChain SWE", "description": "This ticket was created via LangChain SWE pipeline"}

def test_get_tickets():
    # First, create a ticket
    client.post("/tickets/", json={"title": "Test Ticket via LangChain SWE", "description": "This ticket was created via LangChain SWE pipeline"})
    
    # Now, get the tickets
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == {"title": "Test Ticket via LangChain SWE", "description": "This ticket was created via LangChain SWE pipeline"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Ticket API!"}
```

### Instructions to Run the Application and Tests

1. **Install FastAPI and Uvicorn**:
   Make sure you have FastAPI and Uvicorn installed. You can do this using pip:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the FastAPI Application**:
   You can run the FastAPI application using Uvicorn:
   ```bash
   uvicorn app:app --reload
   ```

3. **Install Pytest**:
   If you haven't installed pytest yet, you can do so with:
   ```bash
   pip install pytest
   ```

4. **Run the Tests**:
   You can run the tests using the following command:
   ```bash
   pytest test_app.py
   ```

This setup provides a simple FastAPI application that allows you to create and retrieve tickets, along with unit tests to verify the functionality.