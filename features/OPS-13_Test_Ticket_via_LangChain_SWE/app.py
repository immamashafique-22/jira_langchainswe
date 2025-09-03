Certainly! Below is a complete FastAPI application code based on the provided Jira ticket description, along with corresponding unit tests using Pytest.

### FastAPI Application Code

```python
# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Model for the ticket
class Ticket(BaseModel):
    id: int
    title: str
    description: str

# In-memory storage for tickets
tickets_db = []

@app.post("/tickets/", response_model=Ticket)
async def create_ticket(ticket: Ticket):
    # Check if ticket with the same ID already exists
    if any(t.id == ticket.id for t in tickets_db):
        raise HTTPException(status_code=400, detail="Ticket with this ID already exists.")
    
    tickets_db.append(ticket)
    return ticket

@app.get("/tickets/", response_model=List[Ticket])
async def get_tickets():
    return tickets_db

@app.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: int):
    for ticket in tickets_db:
        if ticket.id == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found.")

@app.delete("/tickets/{ticket_id}", response_model=Ticket)
async def delete_ticket(ticket_id: int):
    for index, ticket in enumerate(tickets_db):
        if ticket.id == ticket_id:
            return tickets_db.pop(index)
    raise HTTPException(status_code=404, detail="Ticket not found.")
```

### Unit Tests using Pytest

```python
# test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app, Ticket

client = TestClient(app)

def test_create_ticket():
    response = client.post("/tickets/", json={"id": 1, "title": "Test Ticket", "description": "This ticket was created via LangChain SWE pipeline"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket was created via LangChain SWE pipeline"}

def test_create_ticket_duplicate():
    client.post("/tickets/", json={"id": 1, "title": "Test Ticket", "description": "This ticket was created via LangChain SWE pipeline"})
    response = client.post("/tickets/", json={"id": 1, "title": "Duplicate Ticket", "description": "This should fail."})
    assert response.status_code == 400
    assert response.json() == {"detail": "Ticket with this ID already exists."}

def test_get_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 1  # We have one ticket created

def test_get_ticket():
    response = client.get("/tickets/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket was created via LangChain SWE pipeline"}

def test_get_ticket_not_found():
    response = client.get("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found."}

def test_delete_ticket():
    response = client.delete("/tickets/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket was created via LangChain SWE pipeline"}

def test_delete_ticket_not_found():
    response = client.delete("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found."}
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

This code provides a simple FastAPI application to manage tickets, including creating, retrieving, and deleting tickets, along with unit tests to ensure the functionality works as expected.