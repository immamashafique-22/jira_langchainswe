Certainly! Below is a complete FastAPI application code that simulates a simple API for managing Jira tickets, along with unit tests using Pytest.

### FastAPI Application Code

```python
# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Model for a Jira ticket
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
    ticket = next((t for t in tickets_db if t.id == ticket_id), None)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return ticket

@app.delete("/tickets/{ticket_id}", response_model=Ticket)
async def delete_ticket(ticket_id: int):
    global tickets_db
    ticket = next((t for t in tickets_db if t.id == ticket_id), None)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    
    tickets_db = [t for t in tickets_db if t.id != ticket_id]
    return ticket
```

### Pytest Unit Tests

```python
# test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app, Ticket

client = TestClient(app)

def test_create_ticket():
    response = client.post("/tickets/", json={"id": 1, "title": "Test Ticket", "description": "This ticket was created using Jira API."})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket was created using Jira API."}

def test_create_duplicate_ticket():
    client.post("/tickets/", json={"id": 1, "title": "Test Ticket", "description": "This ticket was created using Jira API."})
    response = client.post("/tickets/", json={"id": 1, "title": "Duplicate Ticket", "description": "This is a duplicate."})
    assert response.status_code == 400
    assert response.json() == {"detail": "Ticket with this ID already exists."}

def test_get_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 1  # We have one ticket

def test_get_ticket():
    response = client.get("/tickets/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket was created using Jira API."}

def test_get_nonexistent_ticket():
    response = client.get("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found."}

def test_delete_ticket():
    response = client.delete("/tickets/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket was created using Jira API."}

def test_delete_nonexistent_ticket():
    response = client.delete("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found."}

def test_get_tickets_after_deletion():
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 0  # No tickets left after deletion
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

This setup provides a simple FastAPI application for managing Jira tickets with basic CRUD operations and corresponding unit tests to ensure functionality.