Sure! Below is a complete FastAPI application code along with unit tests using Pytest based on the provided Jira ticket description.

### FastAPI Application Code

```python
# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Ticket(BaseModel):
    id: int
    title: str
    description: str

# In-memory storage for tickets
tickets_db = []

@app.post("/tickets/", response_model=Ticket)
async def create_ticket(ticket: Ticket):
    # Check if the ticket ID already exists
    if any(t.id == ticket.id for t in tickets_db):
        raise HTTPException(status_code=400, detail="Ticket ID already exists")
    
    tickets_db.append(ticket)
    return ticket

@app.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: int):
    for ticket in tickets_db:
        if ticket.id == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.get("/tickets/", response_model=list[Ticket])
async def list_tickets():
    return tickets_db
```

### Unit Tests

```python
# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from app.main import app, Ticket

client = TestClient(app)

def test_create_ticket():
    response = client.post("/tickets/", json={"id": 1, "title": "Test Ticket", "description": "This ticket was created via LangChain SWE pipeline"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket was created via LangChain SWE pipeline"}

def test_create_ticket_duplicate_id():
    client.post("/tickets/", json={"id": 1, "title": "Test Ticket", "description": "This ticket was created via LangChain SWE pipeline"})
    response = client.post("/tickets/", json={"id": 1, "title": "Another Ticket", "description": "This is another ticket"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Ticket ID already exists"}

def test_get_ticket():
    client.post("/tickets/", json={"id": 2, "title": "Another Test Ticket", "description": "Another description"})
    response = client.get("/tickets/2")
    assert response.status_code == 200
    assert response.json() == {"id": 2, "title": "Another Test Ticket", "description": "Another description"}

def test_get_ticket_not_found():
    response = client.get("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}

def test_list_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### Instructions to Run the Application and Tests

1. **Install FastAPI and Uvicorn**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Install Pytest**:
   ```bash
   pip install pytest
   ```

3. **Run the FastAPI Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Run the Tests**:
   ```bash
   pytest tests/test_main.py
   ```

This code provides a simple FastAPI application that allows you to create, retrieve, and list tickets, along with unit tests to ensure the functionality works as expected.